from __future__ import annotations

import re
from typing import Any, Literal

import ibis.expr.operations as ops
import ibis.expr.types as ir
import networkx as nx
import rustworkx as rx
from ibis.expr.datatypes import DataType

from vinyl.lib.table import VinylTable
from vinyl.lib.utils.graph import rustworkx_to_networkx


class Field:
    _relations: rx.PyDiGraph = rx.PyDiGraph()
    _relations_node_dict: dict[str, int] = {}
    _field_relations: rx.PyDiGraph = rx.PyDiGraph()
    _field_relations_node_dict: dict[str, int] = {}
    _source_class_dict: dict[ir.Table, Any] = {}
    parent_name: str | None
    parent_table: object | None
    name: str | None
    type: DataType | None
    description: str | None
    primary_key: bool
    unique_key: bool
    foreign_key: Field | None
    pii: bool

    def __init__(
        self,
        parent_name: str | None = None,
        parent_table: object | None = None,
        name: str | None = None,
        type: DataType | None = None,
        description: str | None = None,
        primary_key: bool = False,
        unique_key: bool = False,
        foreign_key: Field | None = None,
        pii: bool = False,
    ):
        self.parent_name = parent_name
        self.parent_table = parent_table
        self.name = name
        self.type = type
        self.description = description
        self.primary_key = primary_key
        self.unique_key = unique_key
        self.foreign_key = foreign_key
        self.pii = pii

    def update_source_class(self):
        self._source_class_dict[self.parent_table.tbl] = (
            self.parent_table._source_class
            if hasattr(self.parent_table, "_source_class")
            else None
        )

    def store_relations(self):
        self.add_node(self.parent_table, "relations")
        self.add_node(getattr(self.parent_table, self.name), "field")
        if self.foreign_key is not None:
            # note for below, foriegn key class has been imported, so self.foreign_key is an ibis expression at this point
            foreign_key_table = VinylTable(
                self.foreign_key.op().find(ops.UnboundTable)[0]
            )
            foreign_key_table._source_class = self._source_class_dict.get(
                foreign_key_table.tbl
            )
            foreign_key_table._is_vinyl_source = True
            self.add_edge(
                self.foreign_key.op().find(ops.UnboundTable)[0].to_expr(),
                self.parent_table,
                "relations",
            )
            self.add_edge(
                self.foreign_key, getattr(self.parent_table, self.name), "field"
            )

    def add_node(self, node: ir.Expr, type=Literal["field", "relations"]):
        hashed = str(hash(node._arg))
        if type == "field" and hashed not in self._field_relations_node_dict:
            self._field_relations_node_dict[hashed] = self._field_relations.add_node(
                node
            )
        elif type == "relations" and hashed not in self._relations_node_dict:
            self._relations_node_dict[hashed] = self._relations.add_node(node)

    def add_edge(
        self, node1: ir.Expr, node2: ir.Expr, type=Literal["field", "relations"]
    ):
        for node in [node1, node2]:
            if type == "field":
                self.add_node(node, type)
            elif type == "relations":
                self.add_node(node, type)

        if type == "field":
            self._field_relations.add_edge(
                self._field_relations_node_dict[str(hash(node1._arg))],
                self._field_relations_node_dict[str(hash(node2._arg))],
                1,
            )
        elif type == "relations":
            self._relations.add_edge(
                self._relations_node_dict[str(hash(node1._arg))],
                self._relations_node_dict[str(hash(node._arg))],
                1,
            )

    def asdict(self):
        out = {}
        for k, v in self.__dict__.items():
            if v is not None and k != "_relations" and k != "_field_relations":
                out[k] = v

        return out

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def export_relations_to_networkx(
        cls, shorten_name: bool = True, filter: list[str] | None = None
    ):
        G = rustworkx_to_networkx(cls._relations)
        # make sure node object is passed as data rather than name to prevent issues with renderer
        nx.set_node_attributes(G, {node: node for node in G.nodes()}, "node")

        if shorten_name or filter:
            nx.relabel_nodes(
                G, {node: node.get_name() for node in G.nodes()}, copy=False
            )

        if not filter:
            return G
        else:
            all_nodes = list(G.nodes())
            nodes_in_subgraph: set[str] = set()
            for fil in filter:
                regex = re.compile(fil)
                nodes_to_add = set(node for node in all_nodes if regex.search(node))
                nodes_in_subgraph = nodes_in_subgraph.union(nodes_to_add)

            return G.subgraph(nodes_in_subgraph)
