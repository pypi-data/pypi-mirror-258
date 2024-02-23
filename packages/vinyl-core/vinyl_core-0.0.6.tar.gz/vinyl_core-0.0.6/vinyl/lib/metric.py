import copy
import warnings
from collections.abc import Iterable
from typing import Any, Callable, Sequence, Set

import ibis
import ibis.expr.datatypes as dt
import ibis.expr.types as ir
import ibis.selectors as s
from ibis import _
from ibis.common.deferred import Deferred
from pydantic import BaseModel, ConfigDict

from vinyl.lib.column import (
    VinylColumn,
    VinylColumnList,
    _process_cols_arg,
    column_type,
)
from vinyl.lib.constants import DIMENSION_LABEL, METRIC_LABEL, SCHEMA_LABEL, TS_COL_NAME
from vinyl.lib.enums import FillOptions, WindowType
from vinyl.lib.table import VinylTable
from vinyl.lib.table_methods import _adjust_fill_list, _join_with_removal
from vinyl.lib.temporal import set_timezone
from vinyl.lib.utils.text import split_interval_string


class Metric(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # prevents error tied to ibis types not being fully pydantic compatible
        validate_assignment=(
            False  # don't actually validate yet, will ship in future release
        ),
    )

    tbl: VinylTable
    name: str = ""  # allows pydantic to still work
    ts: Callable[..., Any]
    agg: Callable[..., Any]
    by: column_type
    fill: FillOptions | Callable[..., Any]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # set name
        self.name = VinylColumn(self.tbl.tbl, self.agg, passthrough_deferred=True).name

        # ensure ts is a timestamp
        self.ts = set_timezone(self.tbl.tbl, self.ts)

        # ensure ts name is set to TS_COL_NAME constant
        ts_orig = copy.deepcopy(self.ts)
        self.ts = lambda t: ts_orig(t).name(TS_COL_NAME)

    @property
    def dimension_names(self) -> Set[str]:
        if self.by is None:
            return set()
        vinyl_by = VinylColumnList(self.tbl.tbl, self.by, passthrough_deferred=True)
        return set(vinyl_by.names)

    def to_dict(self):
        return {
            "tbl": self.tbl,
            "name": self.name,
            "agg": self.agg,
            "ts": self.ts,
            "by": self.by,
            "fill": self.fill,
        }


def get_dimension_names(metrics: Sequence[Metric]) -> Set[str]:
    return set().union(*[m.dimension_names for m in metrics])


class MetricStore:
    all_metrics_dict: dict[str, Metric] = dict()
    all_dimension_names: set[str] = set()

    mutable: bool
    default_tbl: VinylTable | None
    trailing_intervals: list[ibis.interval] | None
    metrics_dict: dict[str, Metric]
    dimension_names: set[str]

    # key will always be a vinylTable, but can't use it here due to a circular reference
    tbl_dict: dict[VinylTable, dict[str, Any]] = {}

    def __init__(
        self,
        metrics: Sequence[Metric] = [],
        default_tbl: VinylTable | None = None,
    ):
        self.mutable = False
        self.default_tbl = default_tbl
        self.trailing_intervals = None
        self.metrics_dict = {m.name: m for m in metrics}
        self.dimension_names = get_dimension_names(metrics)

        self.tbl_dict = {}
        for m in metrics:
            if m.tbl not in self.tbl_dict:
                self.tbl_dict[m.tbl] = {}
                self.tbl_dict[m.tbl][METRIC_LABEL] = set()
                self.tbl_dict[m.tbl][DIMENSION_LABEL] = set()
                self.tbl_dict[m.tbl][SCHEMA_LABEL] = {}

            self.tbl_dict[m.tbl][METRIC_LABEL].add(m.name)
            self.tbl_dict[m.tbl][DIMENSION_LABEL].update(m.dimension_names)
            col_helper_it = VinylColumn(m.tbl.tbl, m.agg, passthrough_deferred=True)
            self.tbl_dict[m.tbl][SCHEMA_LABEL].setdefault(
                col_helper_it.name, col_helper_it.type
            )
            self.tbl_dict[m.tbl][SCHEMA_LABEL][TS_COL_NAME] = dt.Timestamp()
            if m.by is not None and isinstance(m.by, Iterable):
                for dim in VinylColumnList(m.tbl.tbl, m.by, passthrough_deferred=True):
                    self.tbl_dict[m.tbl][SCHEMA_LABEL].setdefault(dim.name, dim.type)

        MetricStore.address_naming_conflicts(self.metrics_dict)
        MetricStore.append(self.metrics_dict)

        self.set_columns()

    def copy(self):
        return MetricStore(list(self.metrics_dict.values()), self.default_tbl)

    def set_columns(self):
        # set columns
        for i, name in enumerate(["ts", *self.dimension_names, *self.metrics_dict]):
            col = getattr(_, name)
            setattr(self, name, col)
            setattr(self, f"_{i}", col)

    def clear_columns(self):
        for name in self.__dict__.copy():
            if name not in [
                "mutable",
                "default_tbl",
                "trailing_intervals",
                "metrics_dict",
                "dimension_names",
                "tbl_dict",
            ]:
                delattr(self, name)

    def reset_columns(self):
        self.clear_columns()
        self.set_columns()

    def __add__(self, other):
        if not isinstance(other, MetricStore):
            raise ValueError(
                f"Can only add two MetricStores together, not a {type(other)}"
            )
        if self.default_tbl is None:
            return other
        if other.default_tbl is None:
            return self

        if self.default_tbl != other.default_tbl:
            raise ValueError(
                "Can't add two MetricStores with different default tables. Use a join (e.g. tbl1 * tbl2) instead."
            )
        combined_metrics = list(self.metrics_dict.values()) + list(
            other.metrics_dict.values()
        )

        return MetricStore(
            combined_metrics,
            self.default_tbl,
        )

    def __radd__(self, other: "MetricStore") -> "MetricStore":
        return other.__add__(self)

    # Make callable so that @model wrapper works
    def __call__(self):
        return self

    # Make mutable when using in a context manager
    def __enter__(self):
        # Create a copy of the original object and make the object mutable
        new = MetricStore(list(self.metrics_dict.values()), self.default_tbl)
        new.mutable = True
        return new

    def __exit__(self, exc_type, exc_value, traceback):
        # Exit logic here
        pass

    def select(
        self,
        cols: Sequence[Deferred] | dict[str, Deferred],
        trailing: list[int | None] = [None],
    ) -> Any:
        if self.default_tbl is None:
            raise ValueError("Can't select from an empty MetricStore.")
        cols_adj = _process_cols_arg(
            self.default_tbl.tbl, cols, passthrough_deferred=True
        )
        return MetricSelect(self, cols=cols_adj, intervals=trailing).select()

    def metric(
        self,
        tbl: VinylTable,
        cols: ir.Scalar | Sequence[ir.Scalar] | dict[str, ir.Scalar],
        ts: ir.TimestampValue,
        by: Sequence[ir.Value] = [],
        fill: FillOptions = FillOptions.null,  # all metrics have fill
    ):
        vinyl_cols = VinylColumnList(tbl.tbl, cols, passthrough_deferred=True)
        if len(vinyl_cols.cols) == 0:
            raise ValueError("Must provide at least one metric to metric function")

        vinyl_by = VinylColumnList(tbl.tbl, by, passthrough_deferred=True)
        vinyl_ts = VinylColumn(tbl.tbl, ts, passthrough_deferred=True)

        fill_list = _adjust_fill_list(len(vinyl_cols.cols), fill)

        mets = []
        for i, v in enumerate(vinyl_cols):
            met = Metric(
                tbl=tbl,
                agg=v.lambdaized,
                ts=vinyl_ts.lambdaized,
                by=vinyl_by.lambdaized,
                fill=fill_list[i],
            )
            mets.append(met)
        out = MetricStore(mets, tbl)
        combined = self + out
        combined.reset_columns()
        if self.mutable:
            self.__dict__ = combined.__dict__
            self.__dict__["mutable"] = True  # reset mutability to True

        return combined

    def trailing(self, intervals: list[tuple[int, str]] | list[str]):
        if isinstance(intervals[0], str):
            intervals = [split_interval_string(i) for i in intervals]

        ## arguments here should be like (1, "d")
        self.trailing_invervals = [ibis.interval(*i) for i in intervals]

    @classmethod
    def append(cls, new_metrics_dict):
        cls.all_metrics_dict.update(new_metrics_dict)
        cls.all_dimension_names = cls.all_dimension_names | get_dimension_names(
            new_metrics_dict.values()
        )

    @classmethod
    def address_naming_conflicts(cls, new_metrics_dict):
        # set warnings for metric name conflicts
        all_intersections = set(new_metrics_dict.keys()) & set(
            cls.all_metrics_dict.keys()
        )
        nontrivial_intersections = set()
        for i in all_intersections:
            new_metrics_entry = new_metrics_dict[i]
            cls_metrics_entry = cls.all_metrics_dict[i]
            if hash(new_metrics_entry.agg(new_metrics_entry.tbl.tbl)) != hash(
                cls_metrics_entry.agg(cls_metrics_entry.tbl.tbl)
            ):
                nontrivial_intersections.add(i)

        if any(nontrivial_intersections):
            warning_txt = f"\n\nMetric(s) {nontrivial_intersections} already exist in the global metric store. The new metric(s) will overwrite the old metric(s).\n\n Here's how the formulas will change:\n"
            for k, v in new_metrics_dict.items():
                if k in nontrivial_intersections:
                    warning_txt += f"- {k}: {cls.all_metrics_dict[k].agg(cls.all_metrics_dict[k].tbl.tbl)} -> {v.agg(v.tbl.tbl)}\n"
            warnings.warn(message=warning_txt)

        # raise error when metric name conflicts with dimension name
        new_all_metric_names = set(new_metrics_dict.keys()) | set(
            cls.all_metrics_dict.keys()
        )
        new_all_dimension_names = get_dimension_names(new_metrics_dict.values()) | set(
            cls.all_dimension_names
        )

        if any(new_all_metric_names & new_all_dimension_names):
            raise ValueError(
                f"\n\nMetric name(s) {new_all_metric_names} conflict with dimension name(s) {new_all_dimension_names}. Please rename the metric(s) or dimension(s)."
            )


class MetricSelect:
    def __init__(
        self,
        MetricStore: MetricStore,
        cols: list[Deferred],
        intervals: list[int | None] = [None],
    ):
        self.metric_store = MetricStore
        self.intervals = intervals
        self.ts: list[Deferred] = []
        self.dimensions: list[Deferred] = []
        self.temp_dimensions: list[Deferred] = []
        self.temp_metrics: list[Deferred] = []

        # helper to select metrics from the same tbl together as long as they have the same ts
        self.tbl_ts_metrics_to_select: dict[VinylTable, list[Deferred]] = {}

        # helper to store raw metric tables
        self.raw_metric_tbls: list[VinylTable] = []

        self.all_exprs = cols

        # create combined schema
        for i, vals in enumerate(list(self.metric_store.tbl_dict.values())):
            if i == 0:
                self.combined_schema = VinylTable.create_from_schema(vals[SCHEMA_LABEL])
            else:
                self.combined_schema += VinylTable.create_from_schema(
                    vals[SCHEMA_LABEL]
                )

    def _process_unaltered_col(self, col, col_name):
        if col_name in self.metric_store.dimension_names:
            self.dimensions.append(col)
        elif col_name in self.metric_store.metrics_dict:
            met = self.metric_store.metrics_dict[col_name]
            key_it = met.tbl.mutate(met.ts(met.tbl))  # use ts column as unique
            self.tbl_ts_metrics_to_select.setdefault(key_it, set())
            self.tbl_ts_metrics_to_select[key_it].add(col_name)
        elif col_name == TS_COL_NAME:
            raise ValueError(
                "Can't select the raw ts column. Consider using the .truncate() or .bucket() method"
            )
        else:
            raise ValueError(f"{col_name} is not a valid column name")

    def _process_derived_col(self, col, col_name):
        vinyl_col = VinylColumn(
            self.combined_schema.tbl, col, passthrough_deferred=True
        )
        sources = vinyl_col.sources
        source_types = []
        for source in sources:
            if source in self.metric_store.dimension_names:
                source_types.append(DIMENSION_LABEL)
            elif source in self.metric_store.metrics_dict:
                source_types.append(METRIC_LABEL)
            elif source == TS_COL_NAME:
                source_types.append(TS_COL_NAME)
            else:
                raise ValueError(f"{source} is not a valid column name")

            if len(set(source_types)) > 1:
                raise ValueError(
                    "Can't mix metrics and dimensions in the same expression"
                )
            elif source_types[0] == TS_COL_NAME:
                self.ts.append(col)
            elif source_types[0] == DIMENSION_LABEL:
                self.temp_dimensions.append(col)
                # ensure that sources are added to dimensions so derivation works later
                self.dimensions.append(source)
            elif source_types[0] == METRIC_LABEL:
                self.temp_metrics.append(col)
                # ensure that sources are added to metrics so derivation works later
                met_source = self.metric_store.metrics_dict[source]
                key_it = met_source.tbl.mutate(
                    met_source.ts(met_source.tbl)
                )  # use ts column as unique so that the same tables with different ts columns are aggregated separately
                self.tbl_ts_metrics_to_select.setdefault(key_it, set())
                self.tbl_ts_metrics_to_select[key_it].add(source)
            else:
                raise ValueError(f"{col_name} is not a valid column name")

    def process_col(self, col):
        vinyl_col = VinylColumn(
            self.combined_schema.tbl, col, passthrough_deferred=True
        )
        col_name = vinyl_col.name
        mets_to_select = []
        for i in self.tbl_ts_metrics_to_select.values():
            mets_to_select.extend(list(i))
        cur_col_names_helper = [
            d
            for d in list(self.dimensions)
            + list(self.temp_dimensions)
            + list(self.temp_metrics)
            + mets_to_select
        ]
        cur_col_names = VinylColumnList(
            self.combined_schema.tbl, cur_col_names_helper, passthrough_deferred=True
        ).names

        # skip if column is already in dimensions or metrics already selected (including derived)
        if col_name in cur_col_names:
            return

        if vinyl_col.is_unaltered:
            self._process_unaltered_col(vinyl_col.lambdaized, col_name)

        else:
            self._process_derived_col(vinyl_col.lambdaized, col_name)

    def _build_final_tbls(self):
        for interval in self.intervals:
            raw_metric_tbl_interval = []
            mets_rename_dict = {}
            # prepare raw metric tables
            for tbl, met_names in self.tbl_ts_metrics_to_select.items():
                tbl = tbl.copy()  # copy tbl to ensure no mutability issues
                mets_it = [
                    self.metric_store.metrics_dict[name].agg for name in met_names
                ]
                fill_it = [
                    self.metric_store.metrics_dict[name].fill for name in met_names
                ]
                vinyl_cols = VinylColumnList(
                    tbl.tbl, mets_it, passthrough_deferred=True
                )
                source_cols = vinyl_cols.sources_as_deferred_resolved(tbl.tbl)
                vinyl_dims = VinylColumnList(
                    tbl.tbl, self.dimensions, passthrough_deferred=True
                )
                source_dims = vinyl_dims.names_as_deferred
                vinyl_ts = VinylColumn(tbl.tbl, self.ts, passthrough_deferred=True)
                source_ts = [vinyl_ts.name]
                ts_original_source = vinyl_ts.sources

                if interval is None:
                    tbl = tbl.select(
                        source_cols,
                        by=[col(tbl.tbl) for col in self.dimensions],
                        sort=[col(tbl.tbl) for col in self.ts],
                    )

                    out_it = tbl.aggregate(
                        cols=[met(tbl.tbl) for met in mets_it],
                        by=source_dims,
                        sort=source_ts,
                        fill=fill_it,
                    )
                else:
                    tbl = tbl.aggregate_all(
                        col_selector=source_cols,
                        f=lambda x: x.collect(),
                        by=[col(tbl.tbl) for col in self.dimensions],
                        sort=[col(tbl.tbl) for col in self.ts],
                        fill=FillOptions.null,  # trailing metrics only support null fill,
                    )
                    collected_tbl_with_trailing = tbl.select_all(
                        col_selector=vinyl_cols.sources_as_deferred_resolved(tbl.tbl),
                        f=lambda x: x.collect().flatten(),
                        by=[dim(tbl) for dim in source_dims],
                        sort=[vinyl_ts.name_as_deferred_resolved(tbl)],
                        window_type=WindowType.rows,
                        window_bounds=(-interval, 0),
                        rename=False,
                    )

                    ## NOTE: to replace once Vinyl mutate function is written
                    unnested = collected_tbl_with_trailing.mutate_all(
                        col_selector=[s.of_type(dt.Array)],
                        f=[lambda y: y.unnest()],
                        rename=False,
                    ).rename(
                        {v: source_ts[i] for i, v in enumerate(ts_original_source)}
                    )  # rename ts to make sure transformation is available for the fill in next step

                    out_it = unnested.aggregate(
                        cols=[met(unnested.tbl) for met in mets_it],
                        by=[dim(unnested.tbl) for dim in source_dims],
                        sort=[col(unnested.tbl) for col in self.ts],
                        fill=FillOptions.null,
                    )

                    mets_rename_dict.update()

                raw_metric_tbl_interval.append(out_it)

            # join together
            joined_raw_metric_tbl_interval = raw_metric_tbl_interval[0]
            for tbl in raw_metric_tbl_interval[1:]:
                # Takes connection replace of first table, this will fail if there are two different connections in the list
                joined_raw_metric_tbl_interval = VinylTable(
                    _join_with_removal(
                        joined_raw_metric_tbl_interval.tbl, tbl.tbl
                    )._arg,
                    _conn_replace=joined_raw_metric_tbl_interval._conn_replace,
                    _twin_conn_replace=joined_raw_metric_tbl_interval._twin_conn_replace,
                )

            # calculate derived dimensions and metrics
            for col in self.temp_dimensions + self.temp_metrics:
                joined_raw_metric_tbl_interval = joined_raw_metric_tbl_interval.mutate(
                    col(joined_raw_metric_tbl_interval.tbl)
                )

            # reorder to match original requested order
            cols_to_select = [
                col.resolve(joined_raw_metric_tbl_interval)
                for col in VinylColumnList(
                    self.combined_schema.tbl, self.all_exprs, passthrough_deferred=True
                ).names_as_deferred
            ]
            joined_raw_metric_tbl_interval = joined_raw_metric_tbl_interval.select(
                cols_to_select
            )

            # rename trailing metrics
            if interval is not None:
                to_rename = [
                    i.get_name()
                    for i in s.where(
                        lambda x: x.get_name() not in source_ts + vinyl_dims.names
                    ).expand(joined_raw_metric_tbl_interval.tbl)
                ]
                joined_raw_metric_tbl_interval = joined_raw_metric_tbl_interval.rename(
                    {f"{v}_{interval}": v for v in to_rename}
                )
            self.raw_metric_tbls.append(joined_raw_metric_tbl_interval)

    def select(self):
        for col in self.all_exprs:
            self.process_col(col)

        # build raw metric tables
        self._build_final_tbls()

        # join raw metric tables
        joined_raw_metric_tbl = self.raw_metric_tbls[0]
        for tbl in self.raw_metric_tbls[1:]:
            # Takes connection replace of first table, this will fail if there are two different connections in the list
            joined_raw_metric_tbl = VinylTable(
                _join_with_removal(joined_raw_metric_tbl.tbl, tbl.tbl)._arg,
                _conn_replace=joined_raw_metric_tbl._conn_replace,
                _twin_conn_replace=joined_raw_metric_tbl._twin_conn_replace,
            )

        # sort outputs
        final = joined_raw_metric_tbl.sort(s.all())

        return final
