import os
from typing import Dict, Generator, List, Tuple, Type, TypeVar, Union

import networkx as nx

import pydot

from ...utils import SkyGenerator, sky_generator


class DigraphWrapper:
    def __init__(self, graph) -> None:
        self.graph: nx.DiGraph = graph
        self.node_exprs: dict[str, "DDGNodeRoot"] = {}
        for node_id in self.graph.nodes:
            label = self.graph.nodes[node_id]["label"]
            # try:
            if label.lstrip("(").startswith(
                ("METHOD,", "METHOD_RETURN,", "UNKNOWN", "RETURN,")
            ):
                expr = "DDGNodeRoot"(label.lstrip(
                    "(").split(",")[0].strip(), None)
                self.node_exprs[node_id] = expr
            else:
                self.node_exprs[node_id] = parse(label)
                assert self.node_exprs[node_id] is not None
            # except:
            #     import traceback

            #     traceback.print_exc()
            #     self.node_exprs[node_id] = None

    @property
    def nodes(self):
        return self.graph.nodes

    @sky_generator
    def iter_nodes(self) -> Generator[Tuple[str, "DDGNodeRoot"], None, None]:
        for node_id in self.graph.nodes:
            yield node_id, self.node_exprs[node_id]


class CFG(DigraphWrapper):
    def __init__(self, graph) -> None:
        super().__init__(graph)

    def entry_node(self) -> str:
        entry, *_ = filter(lambda x: x[1] == 0, self.graph.in_degree)
        return entry[0]

    def exit_node(self) -> str:
        exit, *_ = filter(lambda x: x[1] == 0, self.graph.out_degree)
        return exit[0]


class DDG(DigraphWrapper):
    def __init__(self, graph) -> None:
        super().__init__(graph)


GraphTypes = Union[CFG, DDG]
GraphType = TypeVar("GraphType", CFG, DDG)


def load_graph_from_dot(dot_file: str, graph_cls: Type[GraphType]) -> GraphType:
    # tempjson = tempfile.NamedTemporaryFile()
    cmd = f"node .\parse_dot.js --dotFile {dot_file} -o temp.json"
    os.system(cmd)
    return graph_cls(load_graph("temp.json"))


# def load_graph(json_file: str) -> nx.DiGraph:
#     G = nx.DiGraph()
#     with open(json_file, "r") as f:
#         d = json.load(f)
#         print(d)
#         nodes, edges = d["nodes"], d["edges"]
#         nodes_map = {n["id"]: n["attributes"] for n in nodes}
#         for edge in edges:
#             G.add_edge(edge["source"], edge["target"], **edge["attributes"])
#         for node in G.nodes:
#             attrs_dict = nodes_map[node]
#             G.nodes[node]["label"] = attrs_dict["label"]
#             G.nodes[node]["line"] = int(attrs_dict["line"])
#             # G.attr
#     print(G)
#     return G


NodeLabelType = Union[int, str]


# def label_similarity(label1, label2):
#     return 1 - distance(label1, label2) / max(len(label1), len(label2))


def map_nodes(graph1, graph2) -> Dict[NodeLabelType, NodeLabelType]:
    distances: Dict[str, List[Tuple[NodeLabelType, float]]] = {}
    for g1_node in graph1.nodes:
        if g1_node not in distances:
            distances[g1_node] = []
        for g2_node in graph2.nodes:
            distances[g1_node].append(
                (
                    g2_node,
                    label_similarity(
                        graph1.nodes[g1_node]["label"], graph2.nodes[g2_node]["label"]
                    ),
                )
            )
    print(distances)

    nodes_map = {
        k: sorted(v, key=lambda item: item[1], reverse=True)[0][0]
        for k, v in distances.items()
    }
    return nodes_map


def parse_cpg_dot_file(filename: str, encoding: str = 'utf8') -> List[pydot.Dot]:
    with open(filename, encoding=encoding) as f:
        return parse_cpg_dot(f.read())


def parse_cpg_dot(dot_str: str) -> List[pydot.Dot]:
    return pydot.graph_from_dot_data(dot_str)


def cpg_dot_to_network(dot_graph: pydot.Dot):
    nx.DiGraph()
    edges = (
        SkyGenerator(dot_graph.get_edge_list())
        .cast(pydot.Edge)
        .map(
            lambda edge: (
                edge.get_source(),
                edge.get_destination(),
                edge.obj_dict["attributes"].get("label"),
            )
        )
        .f
    )
    nodes = (
        SkyGenerator(dot_graph.get_node_list())
        .cast(pydot.Node)
        .map(lambda node: (node.get_name(), node.obj_dict["attributes"].get("label")))
        .f
    )
    # print(nodes.l)
    # print(edges.l)
    return nodes.l, edges.l
    # print([(l.get_source(), l.get_destination()) for l in g[0].get_edge_list()])
    # print([d.get_label() for d in g[0].get_node_list()])
