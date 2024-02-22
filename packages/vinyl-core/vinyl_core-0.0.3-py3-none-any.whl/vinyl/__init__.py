from __future__ import annotations

import builtins
from typing import TypeAlias

import ibis.expr.datatypes as types  # noqa: F401
import ibis.selectors as sel  # noqa: F401
import rich
from ibis import _  # noqa: F401

from vinyl.lib.asset import (  # noqa: F401
    metric,
    model,
    resource,  # noqa: F401
)
from vinyl.lib.definitions import load_defs  # noqa: F401
from vinyl.lib.enums import FillOptions  # noqa: F401,
from vinyl.lib.expressions import case, if_else  # noqa: F401
from vinyl.lib.field import Field  # noqa: F401
from vinyl.lib.metric import MetricStore  # noqa: F401
from vinyl.lib.operators import ilike, is_, isin, isnt, like, notin  # noqa: F401
from vinyl.lib.source import source  # noqa: F401
from vinyl.lib.table import VinylTable  # noqa: F401

builtins.print = rich.print  # type: ignore

T: TypeAlias = VinylTable
M: TypeAlias = MetricStore
