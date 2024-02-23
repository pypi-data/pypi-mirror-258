from __future__ import annotations

import pickle as pkl
from functools import reduce, wraps
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Literal, Sequence

import ibis
import ibis.common.exceptions as com
import ibis.expr.operations as ops
import ibis.expr.types as ir
import ibis.selectors as s
import sqlglot
from ibis import Schema, _
from sqlglot.optimizer import optimize
from sqlglot.optimizer.eliminate_ctes import eliminate_ctes
from sqlglot.optimizer.eliminate_joins import eliminate_joins
from sqlglot.optimizer.eliminate_subqueries import eliminate_subqueries
from sqlglot.optimizer.normalize import normalize
from sqlglot.optimizer.pushdown_predicates import pushdown_predicates
from sqlglot.optimizer.pushdown_projections import pushdown_projections
from sqlglot.optimizer.unnest_subqueries import unnest_subqueries

from vinyl.lib.column import (
    VinylColumn,
    VinylColumnList,
    VinylSortColumnList,
    base_boolean_column_type,
    base_column_type,
    boolean_column_type,
    column_type,
    column_type_all,
    column_type_without_dict,
)
from vinyl.lib.enums import FillOptions, WindowType
from vinyl.lib.graph import unify_backends
from vinyl.lib.schema import VinylSchema
from vinyl.lib.table_methods import (
    _adjust_fill_list,
    _build_spine,
    _difference_two,
    _join_spine,
    _process_multiple_select,
    _union_two,
    fill_type,
)
from vinyl.lib.utils.functions import validate

if TYPE_CHECKING:
    from vinyl.lib.chart import geom

RULES = (
    # qualify,
    pushdown_projections,
    normalize,
    unnest_subqueries,
    pushdown_predicates,
    # optimize_joins,  # produces incorrect results
    eliminate_subqueries,
    # merge_subqueries,  # produces incorrect results
    eliminate_joins,
    eliminate_ctes,
    # quote_identifiers,
    # annotate_types,
    # canonicalize,
    # simplify,
)


def ensure_output(func):
    @wraps(func)
    def wrapper(self: VinylTable, *args, **kwargs) -> VinylTable:
        # cache current objects if immutable
        if not self.mutable:
            cached_arg = self._arg
            cached_conn_replace = self._conn_replace
            cached_twin_conn_replace = self._twin_conn_replace

        # build the connection dict and set an updated version to be used in the function
        combined_conn_replace = {}
        combined_twin_conn_replace = {}
        for el in [self, *args, *list(kwargs.values())]:
            if isinstance(el, VinylTable):
                combined_conn_replace.update(el._conn_replace)
                combined_twin_conn_replace.update(el._twin_conn_replace)

        result = func(self, *args, **kwargs)

        if not self.mutable:
            self._arg = cached_arg
            self._conn_replace = cached_conn_replace
            self._twin_conn_replace = cached_twin_conn_replace
        else:
            self._arg = result._arg
            self.mutable = True  # chain mutability to subsequent function calls
            self._conn_replace = combined_conn_replace
            self._twin_conn_replace = combined_twin_conn_replace

        self.reset_columns()

        final = VinylTable(
            result._arg,
            _conn_replace=combined_conn_replace,
            _twin_conn_replace=combined_twin_conn_replace,
        )
        final.mutable = self.mutable
        return final

    return wrapper


class VinylTable:
    _arg: ir.Expr
    mutable: bool
    _conn_replace: dict[ops.Relation, ops.Relation]
    _twin_conn_replace: dict[ops.Relation, ops.Relation]

    def __init__(
        self,
        _arg: ir.Expr,
        _conn_replace: dict[ops.Relation, ops.Relation] = {},
        _twin_conn_replace: dict[ops.Relation, ops.Relation] = {},
    ):
        self._arg = _arg
        self.mutable = False
        self._conn_replace = _conn_replace
        self._twin_conn_replace = _twin_conn_replace
        self.set_columns()

    def set_columns(self, deferred=False):
        # set columns
        for i, (name, type_) in enumerate(self.tbl.schema().items()):
            col = getattr(_, name) if deferred else getattr(self.tbl, name)
            setattr(self, name, col)
            setattr(self, f"_{i}", col)

    def clear_columns(self):
        for name in self.__dict__.copy():
            if name not in ["_arg", "mutable", "_conn_replace", "_twin_conn_replace"]:
                delattr(self, name)

    def reset_columns(self, deferred=False):
        self.clear_columns()
        self.set_columns(deferred=deferred)

    # Make callable so that @model wrapper works
    def __call__(self):
        return self

    def __enter__(self):
        # Create a copy of the original object and make the object mutable
        new = self.copy()
        new.mutable = True
        return new

    def __exit__(self, exc_type, exc_value, traceback):
        # Exit logic here
        pass

    def __str__(self):
        return self.tbl.__str__()

    def __repr__(self):
        return self.tbl.__repr__()

    @property
    def tbl(self):
        return ir.Table(self._arg)

    def copy(self) -> VinylTable:
        return VinylTable(self._arg, self._conn_replace, self._twin_conn_replace)

    @ensure_output
    def __add__(self, other) -> VinylTable:
        # Handle adding CustomNumber to 0, which is the default start value for sum
        if not isinstance(other, VinylTable):
            if other == 0:
                return self

            raise ValueError(
                f"Can only add a VinylTable to another VinylTable, not a {type(other)}"
            )

        return _union_two(self.tbl, other.tbl)

    def __radd__(self, other) -> VinylTable:
        if not isinstance(other, VinylTable):
            raise ValueError(
                f"Can only add a VinylTable to another VinylTable, not a {type(other)}"
            )
        return other.__add__(self)

    @ensure_output
    def __sub__(self, other) -> VinylTable:
        if not isinstance(other, VinylTable):
            raise ValueError(
                f"Can only subtract a VinylTable from another VinylTable, not a {type(other)}"
            )
        return _difference_two(self.tbl, other.tbl)

    def __rsub__(self, other) -> VinylTable:
        if not isinstance(other, VinylTable):
            raise ValueError(
                f"Can only subtract a VinylTable from another VinylTable, not a {type(other)}"
            )
        return other.__sub__(self)

    @ensure_output
    def __mul__(self, other) -> VinylTable:
        if not isinstance(other, VinylTable):
            raise ValueError(
                f"Can only multiply a VinylTable by another VinylTable, not a {type(other)}"
            )

        ## NOTE: for now, we are matching based on the same column names. Will add more advanced joins based on pk/fk later
        common_columns = list(set(self.tbl.columns) & set(other.tbl.columns))
        if len(common_columns) == 0:
            return self.tbl.cross_join(other.tbl)
        else:
            return self.tbl.outer_join(other, predicates=common_columns)

    @ensure_output
    def select(
        self,
        cols: column_type,
        by: column_type | None = None,
        sort: column_type | None = None,  # add support for selectors later
        window_type: WindowType = WindowType.rows,
        window_bounds: tuple[int | None, int | None] = (None, None),
        fill: fill_type = None,
    ) -> VinylTable:
        # get adjusted col names
        vinyl_by = VinylColumnList(self.tbl, by, unique=True)

        # need a copy of sort columns with asc() and desc() applied for sort and one without for selection
        vinyl_sort = VinylSortColumnList(self.tbl, sort, unique=True, reverse=False)

        vinyl_by_and_sort = VinylColumnList(
            self.tbl, vinyl_by.queryable + vinyl_sort.unsorted, unique=True
        )

        vinyl_cols = VinylColumnList(self.tbl, cols, unique=True)

        if (
            len(vinyl_by.queryable) == 0
            and len(vinyl_sort.unsorted) == 0
            and fill is None
        ):
            out = self.tbl.select(*vinyl_cols.queryable)
            return out

        window_ = ibis.window(
            group_by=None if by is None else vinyl_by.queryable,
            order_by=None if sort is None else vinyl_sort.sorted,
            range=(window_bounds if window_type == WindowType.range else None),
            rows=(window_bounds if window_type == WindowType.rows else None),
        )

        source_cols_to_select = VinylColumnList(
            self.tbl, vinyl_by_and_sort.queryable + vinyl_cols.sources_as_deferred
        )

        # Adjust for window
        windowed = vinyl_cols.windowize(window_)
        adj_cols_to_select = vinyl_by_and_sort + windowed

        # make simple selection if no fill or by
        adj_window_ = ibis.window(
            group_by=None if by is None else vinyl_by.names_as_deferred,
            order_by=None if sort is None else vinyl_sort.names_as_deferred_sorted,
            range=(window_bounds if window_type == WindowType.range else None),
            rows=(window_bounds if window_type == WindowType.rows else None),
        )

        if fill is None or len(vinyl_by_and_sort.cols) == 0:
            return self.tbl.select(adj_cols_to_select.queryable)

        # build spine
        spine, rename_dict = _build_spine(self.tbl, vinyl_by_and_sort.queryable)
        fill_list = _adjust_fill_list(len(vinyl_cols.cols), fill)

        # union spine and preaggregated table
        unioned = _join_spine(self.tbl.select(source_cols_to_select.queryable), spine)
        unioned_cols = VinylColumnList(unioned, vinyl_cols.lambdaized, unique=True)
        unioned_cols.windowize(adj_window_, adj_object=True)

        # perform base window calculations
        new_adj_cols_to_select = VinylColumnList(
            unioned,
            vinyl_by.names_as_deferred
            + vinyl_sort.names_as_deferred
            + unioned_cols.queryable,
            unique=True,
        )  # recreate windows with original cols

        filled = unioned.select(*new_adj_cols_to_select.queryable).rename(rename_dict)

        if all([i == FillOptions.null for i in fill_list]):
            if vinyl_sort.cols == []:
                return filled
            return filled.order_by(vinyl_sort.names_as_deferred_sorted)

        for i, col in enumerate(vinyl_cols):
            # switch to VinylTable to access deferred method
            filled = VinylTable(
                filled._arg, self._conn_replace, self._twin_conn_replace
            )
            filled.mutable = self.mutable

            filled = filled._interpolate(
                col.name_as_deferred_resolved(filled),
                sort=vinyl_sort.names_as_deferred_resolved_sorted(filled),
                by=vinyl_by.names_as_deferred_resolved(filled),
                fill=fill_list[i],
            )
        final_sort_cols = vinyl_sort.names_as_deferred_resolved_sorted(
            filled
        ) + vinyl_by.names_as_deferred_resolved(filled)
        if final_sort_cols == []:
            return filled
        return filled.sort(final_sort_cols)

    @ensure_output
    def select_all(
        self,
        col_selector: column_type_all,
        f: Callable[[Any], Any] | list[Callable[[Any], Any] | None] | None,
        by: column_type | None = None,
        sort: column_type | None = None,  # add support for selectors later
        window_type: WindowType = WindowType.rows,
        window_bounds: tuple[int | None, int | None] = (None, None),
        fill: fill_type = None,
        rename: bool = False,
    ) -> VinylTable:
        adj_cols = _process_multiple_select(self.tbl, col_selector, f, rename=rename)
        return self.select(adj_cols, by, sort, window_type, window_bounds, fill)

    @ensure_output
    def mutate(
        self,
        cols: column_type,
        by: column_type | None = None,
        sort: column_type | None = None,  # add support for selectors later
        window_type: WindowType = WindowType.rows,
        window_bounds: tuple[int | None, int | None] = (None, None),
        fill: fill_type = None,
    ) -> VinylTable:
        vinyl_cols = VinylColumnList(self.tbl, cols)
        vinyl_by = VinylColumnList(self.tbl, by)
        vinyl_sort = VinylSortColumnList(self.tbl, sort, reverse=False)

        out = self.select_all(
            col_selector=[s.all()] + vinyl_cols.queryable,
            f=[lambda x: x] + [None] * len(vinyl_cols.queryable),
            by=vinyl_by.queryable,
            sort=vinyl_sort.sorted,
            window_type=window_type,
            window_bounds=window_bounds,
            rename=True,
        )
        return out

    @ensure_output
    def mutate_all(
        self,
        col_selector: column_type_all,
        f: Callable[..., Any] | list[Callable[..., Any] | None] | None,
        by: column_type | None = None,
        sort: column_type | None = None,  # add support for selectors later
        window_type: WindowType = WindowType.rows,
        window_bounds: tuple[int | None, int | None] = (None, None),
        fill: fill_type = None,
        rename: bool = False,
    ) -> VinylTable:
        col_selector_list = (
            [col_selector] if not isinstance(col_selector, list) else col_selector
        )
        f_list = [f] if not isinstance(f, list) else f
        if len(f_list) == 1 and len(col_selector_list) > 1:
            f_list = f_list * len(col_selector_list)

        return self.select_all(
            col_selector=[s.all()]
            + col_selector_list,  # ibis handles renames automtically
            f=[lambda x: x, *f_list],
            by=by,
            sort=sort,
            window_type=window_type,
            window_bounds=window_bounds,
            rename=rename,
        )

    @ensure_output
    def aggregate(
        self,
        cols: column_type,
        by: column_type | None = None,
        sort: column_type | None = None,  # add support for selectors later
        fill: fill_type = None,
    ) -> VinylTable:
        vinyl_cols = VinylColumnList(self.tbl, cols)
        vinyl_by = VinylColumnList(self.tbl, by)
        vinyl_sort = VinylSortColumnList(self.tbl, sort, reverse=False)
        spine_cols = VinylColumnList(
            self.tbl, vinyl_by.queryable + vinyl_sort.unsorted, unique=True
        )
        unadj_tbl = self.tbl.aggregate(
            metrics=vinyl_cols.queryable, by=spine_cols.queryable, having=()
        )

        if fill is None or len(spine_cols.cols) == 0:
            # Don't support having argument. use filter instead
            if vinyl_sort.cols == []:
                return unadj_tbl
            else:
                return unadj_tbl.order_by(vinyl_sort.names_as_deferred_sorted)

        spine, rename_dict = _build_spine(self.tbl, spine_cols.queryable)
        if spine is None:
            return unadj_tbl

        adj_aggregate = unadj_tbl.rename(rename_dict)
        null_fill = _join_spine(
            adj_aggregate, spine
        )  # rejoin spine to ensure all by times/dates are present

        filled = null_fill
        fill_list = _adjust_fill_list(len(vinyl_cols.cols), fill)
        if all([i == FillOptions.null for i in fill_list]):
            if vinyl_sort.cols == []:
                return filled
            return filled.order_by(vinyl_sort.names_as_deferred_sorted)
        # handle factor

        for i, col in enumerate(vinyl_cols):
            # switch to VinylTable to access deferred method
            filled = VinylTable(
                filled._arg, self._conn_replace, self._twin_conn_replace
            )
            filled.mutable = self.mutable
            filled = filled._interpolate(
                col.name_as_deferred_resolved(filled),
                sort=vinyl_sort.names_as_deferred_resolved_sorted(filled),
                by=vinyl_by.names_as_deferred_resolved(filled),
                fill=fill_list[i],
            )
        final_sort_cols = vinyl_sort.names_as_deferred_resolved_sorted(
            filled
        ) + vinyl_by.names_as_deferred_resolved(filled)
        if final_sort_cols == []:
            return filled
        return filled.sort(final_sort_cols)

    def execution_helper(
        self: VinylTable, twin=False, limit: int | None = 10000
    ) -> ir.Table:
        unactivated_conn_replace = (
            self._twin_conn_replace if twin else self._conn_replace
        )
        if unactivated_conn_replace == {} and twin is False:
            raise ValueError(
                "No connection found. Please ensure your connection is correctly set up."
            )
        if unactivated_conn_replace == {} and twin is True:
            raise ValueError(
                "No twin connection found. Please ensure your twin connection is correctly set up."
            )

        # activate conn replace by calling the function
        active_conn_replace = {k: v() for k, v in unactivated_conn_replace.items()}

        replaced = self.tbl.op().replace(active_conn_replace).to_expr()
        replaced = replaced.limit(limit) if limit is not None else replaced

        # handle queries with multiple backends
        if len(replaced._find_backends()[0]) > 1:
            return unify_backends(replaced)
        return replaced

    def execute(
        self,
        format: Literal["pandas", "polars", "pyarrow", "torch"] = "pandas",
        twin: bool = False,
        limit: int | None = 10000,
    ) -> Any:
        replaced = self.execution_helper(twin, limit)
        if format == "pandas":
            return (
                replaced.to_pyarrow().to_pandas()
            )  # normal ibis execute produces type errors which this resolves
        elif format == "pyarrow":
            return replaced.to_pyarrow()
        elif format == "polars":
            try:
                import polars as pl
            except ImportError:
                raise ImportError(
                    "Polars not installed. Please install polars to use it."
                )
            return pl.from_arrow(replaced.to_pyarrow())
        elif format == "torch":
            return replaced.to_torch()
        else:
            raise ValueError(f"Output type {format} not supported")

    def save(
        self,
        path: str | Path,
        format: Literal["csv", "delta", "json", "parquet"] = "csv",
        limit=10000,
    ):
        replaced = self.execution_helper(limit)

        if format == "csv":
            replaced.to_csv(path)
        elif format == "delta":
            replaced.to_delta(path)
        elif format == "json":
            with open(path, "w") as f:
                f.write(replaced.execute().to_json(orient="records"))
        elif format == "parquet":
            replaced.to_parquet(path)
        else:
            raise ValueError(f"Output type {format} not supported")

    def pickle(self, path: str | Path, tbl_only=True):
        if tbl_only:
            pkl.dump(self.tbl, open(path, "wb"))
        else:
            pkl.dump(self, open(path, "wb"))
        return

    @ensure_output
    def aggregate_all(
        self,
        col_selector: column_type_all,
        f: Callable[[Any], Any] | list[Callable[[Any], Any] | None] | None,
        by: column_type | None = None,
        sort: column_type | None = None,  # add support for selectors later
        fill: fill_type = None,
        rename: bool = False,
    ) -> VinylTable:
        adj_cols = _process_multiple_select(self.tbl, col_selector, f, rename=rename)
        return self.aggregate(cols=adj_cols, by=by, sort=sort, fill=fill)

    @ensure_output
    def rename(self, rename_dict: dict[str, str]) -> VinylTable:
        return self.tbl.rename(rename_dict)

    @ensure_output
    def relocate(
        self,
        cols: column_type_without_dict,
        before: base_column_type | s.Selector | None = None,
        after: base_column_type | s.Selector | None = None,
    ) -> VinylTable:
        vinyl_cols = VinylColumnList(self.tbl, cols)
        vinyl_before = VinylColumnList(self.tbl, before) if before is not None else None
        vinyl_after = VinylColumnList(self.tbl, after) if after is not None else None
        before_names = vinyl_before.names if vinyl_before is not None else []
        after_names = vinyl_after.names if vinyl_after is not None else []

        helper = []
        for ls in [before_names, after_names]:
            if len(ls) > 1:
                helper.append(~s.c(*ls))
            elif len(ls) == 1:
                helper.append(ls[0])
            else:
                helper.append(None)

        return self.tbl.relocate(*vinyl_cols.names, before=helper[0], after=helper[1])

    @ensure_output
    def _interpolate(
        self,  # should already have had null fill applied
        cols: column_type | None = None,
        sort: column_type | None = None,
        by: column_type | None = None,
        fill: fill_type = FillOptions.null,  # can specify one of the fill options or a lambda function
    ) -> VinylTable:
        vinyl_cols = VinylColumnList(self.tbl, cols)
        vinyl_by = VinylColumnList(self.tbl, by)
        vinyl_sort = VinylSortColumnList(
            self.tbl, sort, reverse=True if fill == FillOptions.previous else False
        )
        out: VinylTable = self
        adj_fill = _adjust_fill_list(len(vinyl_cols.cols), fill)
        for i, vinyl_col in enumerate(vinyl_cols.cols):
            fill = adj_fill[i]
            if fill is None:
                continue
            elif fill == FillOptions.null:
                out = out.sort(vinyl_sort.sorted)
                # no need to fill further, should already have n
                continue
            elif callable(fill):
                # initial mutate to allow fill to operate on unaltered columns
                fill_col_name = f"fill_{vinyl_col.name}"
                filled_col = fill(vinyl_col.name_as_deferred_resolved(self))
                if not isinstance(filled_col, ir.Expr):
                    filled_col = ibis.literal(filled_col)

                out = out.mutate(
                    {fill_col_name: filled_col},
                    by=vinyl_by.names_as_deferred_resolved(out),
                    sort=vinyl_sort.names_as_deferred_resolved_sorted(out),
                )

                fill_col = VinylColumn(out.tbl, fill_col_name)
                out = out.mutate_all(
                    vinyl_col.name_as_deferred_resolved(out),
                    f=lambda x: x.fillna(fill_col.name_as_deferred_resolved(out)),
                    by=vinyl_by.names_as_deferred_resolved(out),
                    sort=vinyl_sort.sorted,
                )
                out = out.drop(fill_col.name_as_deferred_resolved(out))
            else:
                if sort is None:
                    raise ValueError(
                        "Must provide a sort column when using next or previous fill"
                    )
                helper_col_string = f"helper_{vinyl_col.name}"
                out = self.mutate(
                    {
                        helper_col_string: vinyl_col.name_as_deferred_resolved(
                            out
                        ).count()
                    },
                    by=vinyl_by.names_as_deferred_resolved(out),
                    sort=vinyl_sort.names_as_deferred_resolved_sorted(out),
                    fill=None,
                    window_type=WindowType.rows,
                    window_bounds=(None, 0),
                )
                helper_col = VinylColumn(out.tbl, helper_col_string)
                out = out.mutate(
                    {vinyl_col.name: vinyl_col.name_as_deferred_resolved(out).max()},
                    by=vinyl_by.names_as_deferred_resolved(out)
                    + [helper_col.name_as_deferred_resolved(out)],
                )
                out = out.drop(helper_col.name_as_deferred_resolved(out))
                out = out.sort(vinyl_sort.names_as_deferred_resolved_sorted(out))

        return out

    def chart(
        self,
        geoms: geom
        | list[
            Any
        ],  # always will be a geom, but listing any here to avoid import of lets-plot unless necessary
        x: ir.Value | None,
        y: ir.Value | None = None,
        color: ir.Value | None = None,
        fill: ir.Value | None = None,
        size: ir.Value | None = None,
        alpha: ir.Value | None = None,
        facet: ir.Value | list[ir.Value] | None = None,
        coord_flip: bool = False,
    ):
        from vinyl.lib.chart import BaseChart

        return BaseChart(
            geoms, self, x, y, color, fill, size, alpha, facet, coord_flip
        ).show()

    ## modified version of ibis.sql that modifies sqlglot behavior to (1) minimize parsing and (2) optimize if requested
    def to_sql(self, dialect="duckdb", optimized=False, formatted=True) -> str:
        expr = self.tbl
        if dialect is None:
            try:
                backend = expr._find_backend()
            except com.IbisError:
                # default to duckdb for sqlalchemy compilation because it supports
                # the widest array of ibis features for SQL backends
                backend = ibis.duckdb
            else:
                sqlglot_dialect = getattr(backend, "_sqlglot_dialect", backend.name)
        else:
            try:
                backend = getattr(ibis, dialect)
            except AttributeError:
                raise ValueError(f"Unknown dialect {dialect}")
            else:
                sqlglot_dialect = getattr(backend, "_sqlglot_dialect", dialect)

        sql = backend._to_sql(expr)
        if optimized:
            return optimize(sql, dialect=sqlglot_dialect, rules=RULES).sql(
                dialect=sqlglot_dialect, pretty=True
            )
        elif formatted:
            parsed = sqlglot.parse(sql, dialect=sqlglot_dialect)[0]
            if parsed is not None:
                return parsed.sql(dialect=sqlglot_dialect, pretty=True)
            else:
                raise ValueError("Could not parse SQL")

        return sql

    @ensure_output
    def distinct(
        self,
        on: column_type_without_dict | None = None,
        keep: Literal["first", "last"] | None = "first",
    ) -> VinylTable:
        if on is not None:
            on = VinylColumnList(self.tbl, on, unique=True).names
        return self.tbl.distinct(on=on, keep=keep)

    @ensure_output
    def drop(self, cols: column_type_without_dict) -> VinylTable:
        vinyl_cols = VinylColumnList(self.tbl, cols)
        return self.select(~s._to_selector(vinyl_cols.names))

    @ensure_output
    def dropna(
        self,
        on: column_type_without_dict | None = None,
        how: Literal["any", "all"] = "any",
    ) -> VinylTable:
        if on is not None:
            on = VinylColumnList(self.tbl, on, unique=True).names
        return self.tbl.dropna(subset=on, how=how)

    @ensure_output
    def sort(
        self,
        by: column_type | None = None,
    ) -> VinylTable:
        if by is None:
            return self.tbl
        return self.tbl.order_by(by)

    @ensure_output
    def limit(self, n: int | None, offset: int = 0) -> VinylTable:
        return self.tbl.limit(n, offset)

    @ensure_output
    def join(
        self,
        right: Any,  # will be a VinylTable, but pydantic can't validate
        predicates: (
            str
            | Sequence[
                str
                | ir.BooleanColumn
                | Literal[True]
                | Literal[False]
                | tuple[
                    str | ir.Column,
                    str | ir.Column,
                ]
            ]
        ) = (),
        how: Literal[
            "inner",
            "left",
            "outer",
            "right",
            "semi",
            "anti",
            "any_inner",
            "any_left",
            "left_semi",
        ] = "inner",
        lname: str = "",
        rname: str = "{name}_right",
    ) -> VinylTable:
        return ibis.join(
            left=self.tbl,
            right=right.tbl,
            predicates=predicates,
            how=how,
            lname=lname,
            rname=rname,
        )

    @ensure_output
    def union(self, *rest: Any, distinct: bool = False) -> VinylTable:
        if len(rest) == 0:
            return self

        return reduce(lambda x, y: _union_two(x.tbl, y.tbl, distinct), rest, self)

    @ensure_output
    def filter(self, conditions: boolean_column_type) -> VinylTable:
        return self.tbl.filter(conditions)

    def filter_all(
        self,
        col_selector: column_type_all,
        condition_f: Callable[..., Any] | list[Callable[..., Any] | None] | None,
        condition_type: Literal["and", "or"] = "and",
    ) -> VinylTable:
        adj_cols = _process_multiple_select(
            self.tbl, col_selector, condition_f, rename=False
        )
        if condition_type == "and":
            return self.filter(adj_cols)
        else:
            for i, col in enumerate(adj_cols):
                if i == 0:
                    combined_cond = col
                else:
                    combined_cond |= col
            return self.filter(combined_cond)

    @ensure_output
    def count(
        self, where: base_boolean_column_type | None = None, distinct: bool = False
    ) -> VinylTable:
        vinyl_where = VinylColumn(self.tbl, where)
        if distinct:
            return self.tbl.nunique(where=vinyl_where.col).as_table()
        return self.tbl.count(where=vinyl_where.col).as_table()

    def schema(self) -> VinylSchema:
        ibis_schema = VinylSchema(self.tbl.schema())
        return ibis_schema

    def get_name(self):
        return self.tbl.get_name()

    @property
    def columns(self):
        return self.tbl.columns

    @classmethod
    def create_from_schema(cls, schema: Schema, name: str | None = None, conn=None):
        return cls(ibis.table(schema, name=name)._arg)


# Add pydantic validations. Need to do after function definition to make sure return class (VinylTable) is available to pydantic
VinylTable.select = validate(VinylTable.select)  # type: ignore[method-assign]
VinylTable.select_all = validate(VinylTable.select_all)  # type: ignore[method-assign]
VinylTable.mutate = validate(VinylTable.mutate)  # type: ignore[method-assign]
VinylTable.mutate_all = validate(VinylTable.mutate_all)  # type: ignore[method-assign]
VinylTable.aggregate = validate(VinylTable.aggregate)  # type: ignore[method-assign]
VinylTable.aggregate_all = validate(VinylTable.aggregate_all)  # type: ignore[method-assign]
VinylTable.rename = validate(VinylTable.rename)  # type: ignore[method-assign]
VinylTable.relocate = validate(VinylTable.relocate)  # type: ignore[method-assign]
VinylTable._interpolate = validate(VinylTable._interpolate)  # type: ignore[method-assign]
VinylTable.distinct = validate(VinylTable.distinct)  # type: ignore[method-assign]
VinylTable.drop = validate(VinylTable.drop)  # type: ignore[method-assign]
VinylTable.dropna = validate(VinylTable.dropna)  # type: ignore[method-assign]
VinylTable.sort = validate(VinylTable.sort)  # type: ignore[method-assign]
VinylTable.limit = validate(VinylTable.limit)  # type: ignore[method-assign]
VinylTable.join = validate(VinylTable.join)  # type: ignore[method-assign]
VinylTable.union = validate(VinylTable.union)  # type: ignore[method-assign]
VinylTable.filter = validate(VinylTable.filter)  # type: ignore[method-assign]
VinylTable.filter_all = validate(VinylTable.filter_all)  # type: ignore[method-assign]
VinylTable.count = validate(VinylTable.count)  # type: ignore[method-assign]
