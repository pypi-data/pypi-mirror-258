import contextlib
from typing import Any, Callable

import ibis
import ibis.common.exceptions as com
import ibis.expr.operations as ops
import networkx as nx
import rustworkx as rx
from rich.markup import escape
from rich.text import Text

from vinyl.lib.utils.graphics import adjust_type


def rustworkx_to_networkx(
    graph: rx.PyDiGraph,
    pre_convert: Callable[..., Any] | None = None,
    post_convert: Callable[..., Any] | None = None,
) -> nx.DiGraph:
    """Converts a rustworkx graph to a networkx graph."""
    g = nx.DiGraph()
    cur_nodes = graph.nodes()
    if pre_convert is not None:
        cur_nodes = [pre_convert(i) for i in cur_nodes]
    cur_edges = [(cur_nodes[u], cur_nodes[v]) for u, v in graph.edge_list()]
    g.add_nodes_from(nodes_for_adding=cur_nodes)
    g.add_edges_from(cur_edges)

    if post_convert is not None:
        nx.relabel_nodes(g, post_convert, copy=False)
    return g


## NOTE: Made an attempt at a fix here, but need to verify. Necessary because ops.Join is no longer a valid class
def get_type(node):
    with contextlib.suppress(AttributeError, NotImplementedError):
        return adjust_type(node.dtype)

    try:
        schema = node.schema
    except (AttributeError, NotImplementedError):
        # TODO(kszucs): this branch should be removed
        try:
            # As a last resort try get the name of the output_type class
            return node.output_type.__name__
        except (AttributeError, NotImplementedError):
            return "\u2205"  # empty set character
    except com.IbisError:
        assert isinstance(node, ops.JoinChain)
        tables = [node.first.parent]
        tables.extend([n.table.parent for n in node.rest])
        table_names = [getattr(t, "name", None) for t in tables]
        schemas = [t.schema for t in tables]
        pairs = []
        for i, table in enumerate(tables):
            pairs.extend(
                (f"{table_names[i]}.{column}", type)
                for column, type in schemas[i].items()
            )
        schema = ibis.schema(pairs)

    out = Text("\n   ")
    len_loop = len(schema.names)
    for i, (name, type) in enumerate(zip(schema.names, schema.types)):
        out += Text(escape(name), style="italic") + Text(": ") + adjust_type(type)
        if i < len_loop - 1:
            out += Text("\n   ")

    return out


def get_label(node):
    typename = get_type(node)  # Already an escaped string
    name = type(node).__name__
    nodename = (
        node.name
        if isinstance(
            node,
            (
                ops.Literal,
                ops.Field,
                ops.Alias,
                ops.PhysicalTable,
                ops.window.RangeWindowFrame,
            ),
        )
        else None
    )
    if nodename is not None:
        # [TODO] Don't show nodename because it's too long and ruins the image
        if isinstance(node, ops.window.RangeWindowFrame):
            label = Text(escape(name), style="bold")
        else:
            label = (
                Text(escape(nodename), style="italic")
                + Text(": ")
                + Text(escape(name), style="bold")
            )

            if isinstance(node, ops.Relation):
                label += typename
            else:
                label += Text("\n   :: ") + typename

    else:
        label = Text(escape(name), style="bold")
        if isinstance(node, ops.Relation):
            label += typename
        else:
            label += Text("\n   :: ") + typename

    return label
