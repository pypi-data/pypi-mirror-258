import dataclasses
import importlib
from typing import Any, Callable

import ibis.expr.types as ir
import toml

from vinyl.lib.connect import _ResourceConnector
from vinyl.lib.utils.pkg import find_nearest_pyproject_toml_directory


def get_project_module_name():
    root_path = find_nearest_pyproject_toml_directory()
    with open(root_path, "r") as file:
        data = toml.load(file)

    return data["tool"]["vinyl"]["module_name"]


def load_project_module():
    # Backup the original sys.modules

    module_name = get_project_module_name()
    imported_module = importlib.import_module(module_name)
    return imported_module


@dataclasses.dataclass
class Resource:
    name: str
    connector: _ResourceConnector
    def_: Any


class Project:
    resources: list[Resource]
    sources: list[ir.Table]
    models: list[Callable[..., Any]]
    metrics: list[Callable[..., Any]]

    def __init__(
        self,
        resources: list[Any],
        sources: list[ir.Table] | None = None,
        models: list[Any] | None = None,
        metrics: list[Any] | None = None,
    ):
        self.resources = [
            Resource(
                name=resource_def.__name__,
                def_=resource_def,
                connector=resource_def(),
            )
            for resource_def in resources
        ]
        if sources is not None:
            self.sources = sources
        if models is not None:
            self.models = models
        if metrics is not None:
            self.metrics = metrics

    def get_source_objects(self, with_schema=False) -> list[Any]:
        sources = []
        for resource in self.resources:
            try:
                resource_sources = resource.connector.list_sources(with_schema)
                for source in resource_sources:
                    source.parent_resource = resource
                    sources.append(source)
            except Exception as e:
                print(f"Error loading sources from {resource.name}: {e}")
                continue
        return sources

    def get_resource(self, resource_name: str):
        resources = [
            resource for resource in self.resources if resource.name == resource_name
        ]

        if len(resources) == 0:
            raise ValueError(f"Resource {resource_name} not found")

        resource = resources[0]

        return resource

    def get_source(self, source_id: str):
        sources = [source for source in self.sources if source.__name__ == source_id]

        if len(sources) == 0:
            raise ValueError(f"Source {source_id} not found")

        source = sources[0]

        return source

    def get_model(self, model_id: str):
        if self.models is None:
            raise ValueError("No models found")
        models = [model for model in self.models if model.__name__ == model_id]

        if len(models) == 0:
            raise ValueError(f"Model {model_id} not found")

        model = models[0]

        return model()

    def get_metric_store(self, metric_id: str):
        metrics = [metric for metric in self.metrics if metric.__name__ == metric_id]

        if len(metrics) == 0:
            raise ValueError(f"Metric {metric_id} not found")

        metric = metrics[0]

        return metric()

    def get_asset(self, asset_name: str):
        try:
            return self.get_resource(asset_name)
        except (AttributeError, ValueError):
            try:
                return self.get_source(asset_name)
            except (AttributeError, ValueError):
                try:
                    return self.get_model(asset_name)
                except (AttributeError, ValueError):
                    try:
                        self.get_metric_store(asset_name)
                    except (AttributeError, ValueError):
                        raise ValueError(f"Asset {asset_name} not found")
