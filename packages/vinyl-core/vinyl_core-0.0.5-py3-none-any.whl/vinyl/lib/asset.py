import functools
import inspect
from functools import wraps
from typing import Any, Callable

from vinyl.lib.metric import MetricStore
from vinyl.lib.table import VinylTable
from vinyl.lib.utils.functions import validate


@validate
def base(
    deps: object | Callable[..., Any] | list[object | Callable[..., Any]],
    publish: bool = False,
    tags: str | list[str] | None = None,
    asset_type: str = "model",
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            if not isinstance(deps, list):
                deps_adj = [deps]
            else:
                deps_adj = deps
            # Map the positional arguments to the new names
            aliases = [
                param.name for param in inspect.signature(func).parameters.values()
            ]
            if len(aliases) != len(deps_adj):
                raise Exception("Wrong number of arguments")

            new_kwargs = {}
            for i, alias in enumerate(aliases):
                # TODO: this is a hack to avoid mutable sources and models from being impacted downstream
                # we should eventually clean this up as it's not a sustainable solution
                dep_it = deps_adj[i]()

                if isinstance(dep_it, (VinylTable, MetricStore)):
                    par = dep_it.copy()

                else:
                    raise ValueError(
                        f"Dependencies must be VinylTable or MetricStore, not {type(dep_it)}"
                    )

                par.mutable = True
                new_kwargs[alias] = par

            # Call the original function with the new arguments
            return func(**new_kwargs)

        setattr(wrapper, f"_is_vinyl_{asset_type}", True)

        return wrapper

    return decorator


@validate
def model(
    deps: object | Callable[..., Any] | list[object | Callable[..., Any]],
    publish: bool = False,
    tags: str | list[str] | None = None,
):
    return base(deps, publish, tags, asset_type="model")


@validate
def metric(
    deps: object | Callable[..., Any] | list[object | Callable[..., Any]],
    publish: bool = False,
    tags: str | list[str] | None = None,
):
    return base(deps, publish, tags, asset_type="metric_store")


def resource(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)

    decorated_function._is_vinyl_resource = True
    return decorated_function
