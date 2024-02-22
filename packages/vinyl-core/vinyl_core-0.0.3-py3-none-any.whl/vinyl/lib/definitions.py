import dataclasses
import os
from importlib import import_module
from typing import Any

from vinyl.lib.project import get_project_module_name, load_project_module
from vinyl.lib.utils.pkg import (
    find_submodules_names,
)


@dataclasses.dataclass
class Defs:
    resources: list[Any]
    sources: list[Any]
    models: list[Any]
    metrics: list[Any]


def load_defs() -> Defs:
    project_module_name = get_project_module_name()

    modules = []
    modules.append(import_module(f"{project_module_name}.resources"))
    modules.append(import_module(f"{project_module_name}.sources"))
    no_models_vinyl = os.getenv("NO_MODELS_VINYL")
    if no_models_vinyl is None or no_models_vinyl == "False":
        modules.append(import_module(f"{project_module_name}.models"))

    defs_instance = Defs(resources=[], sources=[], models=[], metrics=[])

    for m in modules:
        for name in find_submodules_names(m):
            module = import_module(name)
            for func in dir(module):
                attr = getattr(module, func)
                if func != "_":
                    # order here is important, resources, but be imported before sources
                    for key in ["resource", "source", "model", "metric_store"]:
                        plural_key = key + "s"
                        if hasattr(attr, f"_is_vinyl_{key}"):
                            current = getattr(defs_instance, plural_key)
                            if attr not in current:
                                setattr(
                                    defs_instance,
                                    plural_key,
                                    getattr(defs_instance, plural_key) + [attr],
                                )
    return defs_instance


def load_project_defs() -> Defs:
    imported_module = load_project_module()
    return imported_module.defs
