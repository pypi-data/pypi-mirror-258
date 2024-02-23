import itertools
from pathlib import Path

import toml


def get_root():
    # Create a Path object for the start directory
    path = Path().resolve()

    # Traverse up through the parent directories
    for parent in itertools.chain([path], path.parents):
        pyproject_toml = parent / "pyproject.toml"
        if pyproject_toml.exists():
            return pyproject_toml.parent.absolute()

    return None


class PyProjectSettings:
    toml: dict

    def __init__(self, path: Path | None = None):
        if path is None:
            path = get_root()
        with open(path / "pyproject.toml") as f:
            self.toml = toml.load(f)

    def get_setting(self, key: str):
        return self.toml["tool"]["vinyl"].get(key, None)
