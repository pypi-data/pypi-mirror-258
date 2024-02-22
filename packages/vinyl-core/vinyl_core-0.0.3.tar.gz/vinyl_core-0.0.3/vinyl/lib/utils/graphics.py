from ibis import Schema
from rich.table import Table
from rich.text import Text
from textual.app import App
from textual.binding import Binding


def adjust_type(type) -> Text:
    if type.is_numeric():
        return Text(str(type), style="yellow")
    elif type.is_string():
        return Text(str(type), style="orange1")
    elif type.is_temporal():
        return Text(str(type), style="cyan")
    elif type.is_boolean():
        return Text(str(type), style="purple")
    elif type.is_json() or type.is_struct() or type.is_array():
        return Text(str(type), style="bright_magenta")
    elif type.is_uuid():
        return Text(str(type), style="medium_purple1")
    elif type.is_geospatial():
        return Text(str(type), style="dark_goldenrod")
    else:
        return Text(str(type))


def print_schema(schema: Schema):
    out = Table()
    out.add_column("#")
    out.add_column("column")
    out.add_column("type")
    for i, (name, type_) in enumerate(schema.items()):
        out.add_row(str(i), str(name), adjust_type(type_))

    return out


class TurntableTextualApp(App):
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit"),
        Binding(key="r", action="reload", description="Reload"),
        Binding(key="d", action="toggle_dark", description="Toggle Dark Mode"),
    ]

    def action_reload(self) -> None:
        self.mount()
