from __future__ import annotations

import copy
from typing import Any, Callable, Sequence, TypeAlias

import ibis
import ibis.common.exceptions as com
import ibis.expr.operations as ops
import ibis.expr.types as ir
from ibis import _
from ibis import selectors as s
from ibis.common.deferred import Deferred

from vinyl.lib.graph import VinylGraph
from vinyl.lib.utils.functions import validate

base_column_type: TypeAlias = str | ir.Value | Callable[..., Any]

base_boolean_column_type: TypeAlias = ir.BooleanValue | Callable[..., Any]
boolean_column_type: TypeAlias = (
    base_boolean_column_type | list[base_boolean_column_type]
)


column_type_without_dict: TypeAlias = (
    base_column_type | s.Selector | list[base_column_type | s.Selector]
)

column_type: TypeAlias = column_type_without_dict | dict[str, base_column_type]

column_type_all: TypeAlias = column_type_without_dict | list[column_type_without_dict]


@validate
def _append_name(col: ir.Value | Deferred, name: str | None = None) -> base_column_type:
    if name is None:
        return col
    try:  # check if v can be named, if it can't, wrap in coalesce
        col_named = col.name(name)
    except Exception:
        col_named = ibis.coalesce(col).name(name)

    return col_named


@validate
def _process_cols_arg(
    tbl: ir.Table,
    cols: column_type | None,
    names: list[str | None] | str | None = None,
    passthrough_deferred=False,
) -> list[ir.Value]:
    out: list[ir.Value] = []
    name = names[0] if isinstance(names, list) else names
    if cols is None:
        pass

    elif isinstance(cols, ir.Value):
        out = [_append_name(cols, name)]

    elif isinstance(cols, str):
        out = [_append_name(getattr(tbl, cols), name)]

    elif isinstance(cols, Deferred):
        if passthrough_deferred:
            out = [_append_name(cols, name)]
        else:
            out = [_append_name(cols.resolve(tbl), name)]

    elif callable(cols):
        if passthrough_deferred:
            out = [lambda t: _append_name(cols(t), name)]
        else:
            out = [_append_name(cols(tbl), name)]

    elif isinstance(cols, s.Selector):
        out = cols.expand(tbl)

    elif isinstance(cols, list):
        for col in cols:
            out.extend(
                _process_cols_arg(tbl, col, passthrough_deferred=passthrough_deferred)
            )

    elif isinstance(cols, dict):
        for name, col in cols.items():
            out.extend(
                _process_cols_arg(
                    tbl, col, name, passthrough_deferred=passthrough_deferred
                )
            )

    return out


class VinylColumn:
    def __init__(
        self,
        tbl: ir.Table,
        col: ir.Value | Sequence[ir.Value | s.Selector] | None,
        passthrough_deferred=False,
    ):
        self.tbl = tbl
        if col is None:
            self.col = None
        else:
            self.col = _process_cols_arg(
                self.tbl, col, passthrough_deferred=passthrough_deferred
            )[0]

    @property
    def name(self):
        if self.col is None:
            return None

        elif isinstance(self.col, str):
            return self.col

        elif isinstance(self.col, Deferred):
            return self.col.resolve(self.tbl).get_name()

        elif callable(self.col):
            return self.col(self.tbl).get_name()

        return self.col.get_name()

    @property
    def type(self):
        if self.col is None:
            return None

        elif isinstance(self.col, str):
            return getattr(self.tbl, self.col).resolve(self.tbl).type()

        elif isinstance(self.col, Deferred):
            return self.col.resolve(self.tbl).type()

        elif callable(self.col):
            return self.col(self.tbl).type()

        return self.col.type()

    @property
    def name_as_deferred(self):
        if self.col is None:
            return None
        return getattr(_, self.name)

    def name_as_deferred_resolved(self, tbl):
        if self.col is None:
            return None
        return getattr(tbl, self.name)

    @property
    def lambdaized(self):
        if isinstance(self.col, Deferred):
            self.col = self.col.resolve(self.tbl)
        elif callable(self.col):
            return self.col
        return lambda t: self.col.op().replace({self.tbl.op(): t.op()}).to_expr()

    @property
    def sources(self):
        if isinstance(self.col, Deferred):
            self.col = self.col.resolve(self.tbl)

        elif callable(self.col):
            self.col = self.col(self.tbl)

        return [i.name for i in self.col.op().find_topmost(ops.Field)]

    @property
    def nodes(self):
        graph = VinylGraph.new_init_from_expr(self.tbl.select(self.col))
        return graph.nodes()

    @property
    def is_unaltered(self):
        allowed = (ops.Field, ops.Relation)
        return all([isinstance(n, allowed) for n in self.nodes])

    @property
    def is_only_aliased(self):
        allowed = (ops.Field, ops.Relation, ops.Alias)
        return all([isinstance(n, allowed) for n in self.nodes])


class VinylColumnList:
    def __init__(
        self,
        tbl: ir.Table,
        cols: dict[str, Deferred | ir.Value]
        | list[Deferred | ir.Value | s.Selector]
        | Deferred
        | ir.Value
        | s.Selector
        | None,
        unique=False,
        passthrough_deferred=False,
    ):
        self.tbl = tbl
        self.unique = unique
        self.cols = []

        cols = _process_cols_arg(
            self.tbl, cols, passthrough_deferred=passthrough_deferred
        )
        if cols is None:
            pass
        elif isinstance(cols, list):
            for col in cols:
                if isinstance(col, s.Selector):
                    self.cols.extend(
                        [
                            VinylColumn(
                                tbl, c, passthrough_deferred=passthrough_deferred
                            )
                            for c in col.expand(self.tbl)
                        ]
                    )
                else:
                    self.cols.append(
                        VinylColumn(tbl, col, passthrough_deferred=passthrough_deferred)
                    )
        else:
            if isinstance(cols, s.Selector):
                self.cols = [
                    VinylColumn(tbl, c, passthrough_deferred=passthrough_deferred)
                    for c in cols.expand(self.tbl)
                ]
            else:
                self.cols = [
                    VinylColumn(tbl, cols, passthrough_deferred=passthrough_deferred)
                ]

        if unique:
            self.make_unique()

    def __iter__(self):
        return iter(self.cols)

    def __add__(self, other):
        if isinstance(other, VinylColumn):
            if self.tbl != other.tbl:
                raise ValueError(
                    "Can only add a VinylColumn to a VinylColumnList from the same VinylTable"
                )
            return VinylColumnList(self.tbl, self.cols.append(other))
        elif not isinstance(other, VinylColumnList):
            raise ValueError(
                f"Can only add a VinylColumnList to another VinylColumnList, not a {type(other)}"
            )

        elif self.tbl.__hash__() != other.tbl.__hash__():
            raise ValueError(
                "Can only add a VinylColumnList to another VinylColumnList from the same VinylTable"
            )

        return VinylColumnList(
            self.tbl,
            [c.col for c in self.cols] + [c.col for c in other.cols],
            unique=self.unique and other.unique,
        )

    def __radd__(self, other):
        if isinstance(other, VinylColumnList):
            return other.__add__(self)

        return self.__add__(other)

    def windowize(self, window_, adj_object=False):
        # ensure col can be windowed
        new_obj = self if adj_object else copy.deepcopy(self)
        for col in new_obj.cols:
            try:
                windowed = col.col.over(window_)
                if isinstance(windowed, Deferred):
                    windowed = windowed.resolve(self.tbl)
                col.col = windowed
            except com.IbisTypeError:
                pass

        return new_obj

    def make_unique(self):
        names = []
        unique_cols = []
        zipped = list(zip(self.names, self.queryable))[
            ::-1
        ]  # reverse so latest iteration of column is kept
        for name, col in zipped:
            if name not in names:
                names.append(name)
                unique_cols.append(col)

        unique_cols = unique_cols[::-1]
        self.cols = [VinylColumn(self.tbl, col) for col in unique_cols]
        self.unique = True

    def reset_tbl(self, tbl):
        self.tbl = tbl

    @property
    def queryable(self):
        return [col.col for col in self.cols if col.col is not None]

    @property
    def lambdaized(self):
        return [col.lambdaized for col in self.cols if col.col is not None]

    @property
    def sources_as_deferred(self):
        return [getattr(_, col) for col in self.get_direct_col_sources(unique=True)]

    def sources_as_deferred_resolved(self, tbl):
        return [getattr(tbl, col) for col in self.get_direct_col_sources(unique=True)]

    @property
    def names(self):
        return [col.name for col in self.cols]

    @property
    def types(self):
        return [col.type for col in self.cols]

    @property
    def names_as_deferred(self):
        return [col.name_as_deferred for col in self.cols]

    def names_as_deferred_resolved(self, tbl):
        return [col.name_as_deferred_resolved(tbl) for col in self.cols]

    def get_direct_col_sources(self, unique=True):
        # ibis table, not vinylTable
        col_sources = []
        for col in self.queryable:
            if isinstance(col, Deferred):
                col = col.resolve(self.tbl)
            if callable(col):
                col = col(self.tbl)
            sel_sources = [i.name for i in col.op().find_topmost(ops.Field)]
            if unique:
                col_sources.extend(sel_sources)
            else:
                col_sources.append(sel_sources)

        if unique:
            col_sources = list(set(col_sources))

        return col_sources


class VinylSortColumnList(VinylColumnList):
    def __init__(
        self, tbl, cols, reverse=False, unique=False, passthrough_deferred=False
    ):
        super().__init__(tbl, cols, unique, passthrough_deferred=passthrough_deferred)
        self.reverse = reverse

    @property
    def sorted(self):
        final = []
        for so in self.cols:
            # columns must be resolved for this to work
            if isinstance(so.col, Deferred):
                so.col = so.col.resolve(self.tbl)
            op_it = so.col.op()
            if isinstance(op_it, ops.SortKey):
                # in this case ops_it is a tuple, where the first key is the column and the second is the sort order bool (true is ascending)
                col_expr = op_it.args[0].to_expr()
                out_it = (
                    col_expr.desc() if op_it.args[1] ^ self.reverse else col_expr.asc()
                )
            else:
                out_it = so.col.desc() if self.reverse else so.col.asc()
            final.append(out_it)

        return final

    @property
    def unsorted(self):
        final = []
        for so in self.cols:
            op_it = so.col.op()
            if isinstance(op_it, ops.SortKey):
                # in this case ops_it is a tuple, where the first key is the column and the second is the sort order bool (true is ascending)
                col_expr = op_it.args[0].to_expr()

            else:
                col_expr = so.col
                # in this case, asc is the default
            final.append(col_expr)

        return final

    @property
    def names_as_deferred_sorted(self):
        directions = self.sort_directions
        return [
            name_def.asc() if directions[i] else name_def.desc()
            for i, name_def in enumerate(self.names_as_deferred)
        ]

    def names_as_deferred_resolved_sorted(self, tbl):
        directions = self.sort_directions
        return [
            name_def.asc() if directions[i] else name_def.desc()
            for i, name_def in enumerate(self.names_as_deferred_resolved(tbl))
        ]

    @property
    def sort_directions(self):
        sort_directions = []
        for so in self.cols:
            op_it = so.col.op()
            if isinstance(op_it, ops.SortKey):
                sort_directions.append(op_it.args[1])
            else:
                sort_directions.append(True)

        return sort_directions
