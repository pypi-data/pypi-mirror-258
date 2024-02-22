import os
import pkgutil
import sys
from contextlib import contextmanager

import toml


@contextmanager
def extend_sys_path(path):
    original_sys_path = list(sys.path)  # Make a copy of the original sys.path
    sys.path.append(path)
    try:
        yield
    finally:
        sys.path = original_sys_path  # Restore the original sys.path


# separating recursion out allows us to only extend sys path temporarily for top-level package
def find_submodule_names_recursion_helper(package):
    """Recursively find all submodules in a nested set of folders for the given package."""
    if isinstance(package, str):
        package = __import__(package, fromlist=[""])

    submodules = []
    for loader, name, is_pkg in pkgutil.walk_packages(
        package.__path__, package.__name__ + "."
    ):
        submodules.append(name)
        # If the current module is a package, recurse into it
        if is_pkg:
            submodules.extend(find_submodule_names_recursion_helper(name))
    return submodules


def find_submodules_names(package):
    if hasattr(package, "__path__"):
        with extend_sys_path(package.__path__[0]):
            return list(set(find_submodule_names_recursion_helper(package)))
    else:
        return [package.__name__]


def find_nearest_pyproject_toml_directory(start_path="."):
    """
    Search for the nearest 'pyproject.toml' starting from 'start_path' and moving up the directory tree.
    Returns the path to 'pyproject.toml' if found, otherwise None.
    """
    current_dir = os.path.abspath(start_path)
    while True:
        file_list = os.listdir(current_dir)
        parent_dir = os.path.dirname(current_dir)
        if "pyproject.toml" in file_list:
            return os.path.join(current_dir, "pyproject.toml")
        elif current_dir == parent_dir:  # If we've reached the root directory
            return None
        else:
            current_dir = parent_dir


def get_project_directory(start_path="."):
    toml_path = find_nearest_pyproject_toml_directory(start_path)
    with open(toml_path, "r") as file:
        data = toml.load(file)
    return os.path.join(
        os.path.dirname(toml_path), data["tool"]["vinyl"]["module_name"]
    )
