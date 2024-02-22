import os
import shutil

import typer

from .preview import preview_cli
from .project import project_cli
from .sources import sources_cli

app = typer.Typer(pretty_exceptions_show_locals=False)
app.add_typer(preview_cli, name="preview")
app.add_typer(sources_cli, name="sources")
app.add_typer(project_cli, name="project")


@app.command("init")
def init_project(project_name: str):
    """Initialize a new Vinyl project"""
    normalized_project_name = project_name.lower().replace(" ", "_")
    scaffolding_path = os.path.join(os.path.dirname(__file__), "_project_scaffolding")
    project_path = os.path.join(os.getcwd(), normalized_project_name)
    if os.path.exists(project_path):
        raise ValueError(f"Directory {project_path} already exists")

    # copy the scaffolding to the new project path
    shutil.copytree(scaffolding_path, project_path)
    # rename the project folder
    os.rename(
        os.path.join(project_path, "__project_name__"),
        os.path.join(project_path, normalized_project_name),
    )

    # delete gitkeep from data
    # TODO
    os.remove(os.path.join(project_path, "data", ".gitkeep"))
    # templatize project assets
    project_assets = [
        "README.md",
        "pyproject.toml",
    ]
    asset_paths = [os.path.join(project_path, asset) for asset in project_assets]
    for path in asset_paths:
        with open(path, "r") as f:
            content = f.read()
        content = content.replace("{{PROJECT_NAME}}", normalized_project_name)
        with open(path, "w") as f:
            f.write(content)

    typer.echo(f"Created project at {project_path}")


if __name__ == "__main__":
    app()
