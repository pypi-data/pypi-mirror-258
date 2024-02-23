from enum import Enum
from typing import Any, Literal

import ibis.expr.types as ir
from ibis.common.deferred import Deferred
from lets_plot import (
    LetsPlot,
    aes,
    coord_flip,
    facet_grid,
    facet_wrap,
    flavor_darcula,
    ggplot,
    scale_x_datetime,
    scale_y_datetime,
)

from vinyl.lib.column import VinylColumn, VinylColumnList
from vinyl.lib.settings import PyProjectSettings


class geom(Enum):
    from lets_plot import (
        geom_area,
        geom_area_ridges,
        geom_bar,
        geom_bin2d,
        geom_boxplot,
        geom_density,
        geom_histogram,
        geom_line,
        geom_point,
        geom_smooth,
        geom_violin,
        position_dodge,
        ylab,
    )

    scatter = geom_point()
    line = geom_line()
    bar = geom_bar(stat="identity", position=position_dodge())
    area = geom_area()
    stacked_bar = geom_bar(stat="identity")
    percent_bar = geom_bar() + aes(y="..prop..") + ylab("Percent of total")
    histogram = geom_histogram()
    histogram_2d = geom_bin2d()
    violin = geom_violin()
    boxplot = geom_boxplot()
    density = geom_density()
    ridge = geom_area_ridges()
    trendline_lm = geom_smooth()
    trendline_loess = geom_smooth(method="loess")


class BaseChart:
    mode: Literal["light", "dark"] = "dark"

    from lets_plot import (
        LetsPlot,
        aes,
        coord_flip,
        facet_grid,
        facet_wrap,
        flavor_darcula,
        ggplot,
        scale_x_datetime,
        scale_y_datetime,
    )

    def __init__(
        self,
        geoms: geom | list[geom],
        source: Any,  # will be VinylTable, but use Any to avoid recursion
        x: Deferred | ir.Value | None,
        y: Deferred | ir.Value | None = None,
        color: Deferred | ir.Value | None = None,
        fill: Deferred | ir.Value | None = None,
        size: Deferred | ir.Value | None = None,
        alpha: Deferred | ir.Value | None = None,
        facet: Deferred | ir.Value | list[Deferred | ir.Value] | None = None,
        coord_flip: bool = False,
    ):
        self.geoms = geoms
        self.data = source
        self.x = x
        self.y = y
        self.color = color
        self.fill = fill
        self.size = size
        self.alpha = alpha
        self.facet = facet
        self.coord_flip = coord_flip

    def show(self):
        LetsPlot.setup_html()
        adj_facet = self.facet if isinstance(self.facet, list) else [self.facet]
        all_cols = [
            x
            for x in [self.x]
            + [self.y]
            + [self.color]
            + [self.fill]
            + [self.size]
            + [self.alpha]
            + adj_facet
            if x is not None
        ]

        adj_data = self.data.mutate(all_cols).execute("pandas")

        ## make sure all cols are in there,
        vinyl_x = VinylColumn(self.data.tbl, self.x)
        type_x = vinyl_x.type
        if self.y is not None:
            vinyl_y = VinylColumn(self.data.tbl, self.y)
            type_y = vinyl_y.type
        aes_dict = {}
        for var in ["x", "y", "color", "fill", "size"]:
            attr = getattr(self, var)
            if attr is not None:
                aes_dict[var] = VinylColumn(self.data.tbl, attr).name

        plot = ggplot(adj_data, aes(**aes_dict))
        if isinstance(self.geoms, list):
            for g in self.geoms:
                plot += g.value
        elif self.geoms is not None:
            plot += self.geoms.value
        if self.facet is not None:
            facet_names = VinylColumnList(self.data.tbl, adj_facet).names
            if len(adj_facet) > 1:
                plot += facet_grid(
                    facet_names[0],
                    facet_names[1],
                )
            else:
                plot += facet_wrap(facet_names[0])
        if type_x.is_timestamp():
            plot += scale_x_datetime()
        if self.y is not None and type_y.is_timestamp():
            plot += scale_y_datetime()
        if self.coord_flip:
            plot += coord_flip()

        if PyProjectSettings().get_setting("dark-mode") is True:
            plot += flavor_darcula()

        return plot
