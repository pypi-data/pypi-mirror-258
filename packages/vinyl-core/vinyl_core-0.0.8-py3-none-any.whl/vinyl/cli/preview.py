import dataclasses

import typer
from textual.app import ComposeResult
from textual.widgets import DataTable, Footer

from vinyl import Field
from vinyl.lib.constants import PreviewHelper
from vinyl.lib.definitions import load_project_defs
from vinyl.lib.erd import create_erd_app
from vinyl.lib.project import Project
from vinyl.lib.utils.graphics import TurntableTextualApp

preview_cli = typer.Typer(pretty_exceptions_show_locals=False)


class PreviewTable(TurntableTextualApp):
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        super().__init__()

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.columns)
        table.add_rows(self.rows)


@preview_cli.command("show")
def preview(
    asset_name: str = typer.Option(
        False, "--name", "-m", help="exported name of the model or source"
    ),
    twin: bool = typer.Option(False, "--twin", "-t", help="use twin data"),
):
    """Preview a model"""
    if twin:
        PreviewHelper.preview = "twin"

    defs = load_project_defs()
    project = Project(**dataclasses.asdict(defs))
    model = project.get_asset(asset_name)
    df = model.limit(100).execute(twin=twin)

    app = PreviewTable(
        columns=tuple(df.columns), rows=[tuple(row) for row in df.to_numpy()]
    )
    app.run()


@preview_cli.command("erd")
def erd(
    names: list[str] = typer.Option(
        [], "--name", "-m", help="exported name(s) of the model or source"
    ),
):
    """Generate an ERD"""
    load_project_defs()
    G = Field.export_relations_to_networkx(
        shorten_name=True, filter=None if len(names) == 0 else names
    )
    create_erd_app(G).run()
