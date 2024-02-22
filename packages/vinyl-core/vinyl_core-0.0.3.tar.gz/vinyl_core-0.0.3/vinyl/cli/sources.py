import os

import typer
from rich.console import Console
from rich.table import Table
from tqdm import tqdm

from vinyl.lib.connect import (
    DatabaseFileConnector,
    Source,
    _DatabaseConnector,
    _FileConnector,
    _TableConnector,
)
from vinyl.lib.definitions import load_project_defs
from vinyl.lib.project import Project, load_project_module
from vinyl.lib.source import _get_twin_relative_path
from vinyl.lib.utils.ast import find_classes_and_attributes, get_imports_from_file_regex
from vinyl.lib.utils.files import create_dirs_with_init_py
from vinyl.lib.utils.functions import with_modified_env
from vinyl.lib.utils.text import make_python_identifier

console = Console()


sources_cli = typer.Typer(pretty_exceptions_show_locals=False)


@sources_cli.command("list")
def list_sources(tables: bool = False):
    """Caches sources to a local directory (default: .turntable/sources)"""
    defs = load_project_defs()
    project = Project(resources=defs.resources, models=defs.models)

    table = Table("Name", "Resource", "Location", title="Sources")
    for source in project.get_source_objects():
        table.add_row(
            f"[bold]{source.name}[bold]",
            f"[grey70]{source.parent_resource.def_.__name__}[grey70]",
            f"[grey70]{source.location}[grey70]",
        )
    console.print(table)


def table_to_python_class(table_name):
    return "".join([word.capitalize() for word in table_name.split("_")])


def source_to_class_string(
    source: Source,
    saved_attributes: dict[str, str],
    generate_twin: bool = False,
    root_path: str = os.path.dirname(load_project_module().__file__),
    sample_size: int = 1000,
):
    class_name = table_to_python_class(source.name)
    class_body = f'    _table = "{source.name}"\n'
    pr = source.parent_resource

    if pr is None:
        raise ValueError("Source must have a parent resource.")

    if isinstance(pr.connector, _TableConnector):
        tbl = pr.connector.get_table(source.location)
        class_body += f'    _unique_name = "{pr.name}.{class_name}"\n'

    elif isinstance(pr.connector, _DatabaseConnector):
        # source is a database
        database, schema = source.location.split(".")
        class_body += f'    _unique_name = "{pr.name}.{source.location}.{class_name}"\n'
        class_body += f'    _schema = "{schema}"\n'
        class_body += f'    _database = "{database}"\n'

        database, schema = source.location.split(".")
        tbl = pr.connector.get_table(database, schema, source.name)
        class_body += f'    _twin_path = "{_get_twin_relative_path(pr.name, database, schema)}"\n\n'
        # need row count if using local files (since sampling is done live from the file)

    else:
        raise NotImplementedError(
            f"Connector type {type(pr.connector)} is not yet supported"
        )

    # need row count if using local files (since sampling is done live from the file)
    if isinstance(pr.connector, _FileConnector):
        if isinstance(pr.connector, DatabaseFileConnector):
            # in this case, location is not the real path, but the database and schema, but we can use the path from the connector
            path = os.path.relpath(pr.connector.path, root_path)
        else:
            path = os.path.relpath(source.location, root_path)
        class_body += f'    _path = "{path}"\n'
        if not pr.connector.remote:
            # in this case, we will not be caching the table, so we need the row_count
            class_body += f"    _row_count = {tbl.count().execute()}\n\n"

    if source.schema is None:
        raise ValueError(f"Schema for {source.name} is not available")

    for col_name, col_type in source.schema.items():
        base = f"    {col_name.lower().replace(' ', '_')}: t.{col_type.__repr__()}"
        if col_name in saved_attributes:
            base += f" = {saved_attributes[col_name]}"
        class_body += f"{base}\n"

    out = f"""class {class_name}:
{class_body}
"""
    return out


def get_save_dir(sources_path: str, source: Source) -> str:
    if source.parent_resource is None:
        raise ValueError("Source must have a parent resource.")
    if isinstance(source.parent_resource.connector, _TableConnector):
        # source is a file
        return os.path.join(sources_path, source.parent_resource.name)
    if isinstance(source.parent_resource.connector, _DatabaseConnector):
        # source is a database
        identifers = [
            make_python_identifier(str_) for str_ in source.location.split(".")
        ]
        return os.path.join(sources_path, source.parent_resource.name, *identifers)
    raise NotImplementedError(
        f"Connector type {type(source.parent_resource.connector)} is not yet supported"
    )


@sources_cli.command("generate")
def generate_sources(
    twin: bool = typer.Option(
        False, "--generate_twin", "-t", help="exported name of the model"
    ),
    resources: list[str] = typer.Option(
        [], "--resource", "-r", help="resource names to select"
    ),
):
    """Generates schema files for sources"""

    @with_modified_env("NO_MODELS_VINYL", "True")
    def run_fn():
        defs = load_project_defs()
        if len(resources) == 0:
            project = Project(resources=defs.resources)
        else:
            project = Project(
                resources=[r for r in defs.resources if r.__name__ in resources]
            )
        root_path = os.path.dirname(load_project_module().__file__)
        sources = project.get_source_objects(with_schema=True)

        sources_path = os.path.join(root_path, "sources")
        create_dirs_with_init_py(sources_path)

        for source in sources:
            save_dir = get_save_dir(sources_path, source)
            create_dirs_with_init_py(save_dir)
            file_path = os.path.join(save_dir, f"{source.name}.py")
            saved_attributes = find_classes_and_attributes(file_path)
            saved_imports = (
                get_imports_from_file_regex(file_path)
                if saved_attributes != {}
                else None
            )
            with open(os.path.join(save_dir, f"{source.name}.py"), "w+") as f:
                if saved_imports:
                    f.write(saved_imports)
                else:
                    f.write("# type: ignore\n")  # prevents pylance errors tied to Ibis
                    f.write("from vinyl import source\n")
                    f.write("from vinyl import types as t\n\n")
                    f.write(
                        f"from {source.parent_resource.def_.__module__} import {source.parent_resource.def_.__name__}\n\n\n"
                    )
                f.write(f"@source(resource={source.parent_resource.name})\n")
                f.write(
                    source_to_class_string(
                        source, saved_attributes, root_path=root_path
                    )
                )

        if twin:
            msg = "generating twins... " if len(sources) > 1 else "generating twin... "
            for source in tqdm(
                sources,
                msg,
                unit="source",
            ):
                pr = source.parent_resource
                if isinstance(pr.connector, _DatabaseConnector):
                    database, schema = source.location.split(".")
                    pr.connector.generate_twin(
                        os.path.join(root_path, _get_twin_relative_path(pr.name)),
                        database,
                        schema,
                        source.name,
                    )
                elif isinstance(pr.connector, _TableConnector):
                    # doesn't actually generate a file, just returns the path
                    pr.connector.generate_twin(source.location)

        print(f"Generated {len(sources)} sources at {sources_path}")

    run_fn()
