from typing import Dict, List

import networkx as nx


def build_call_graph(calls: Dict[str, List[str]]) -> nx.DiGraph:
    """
    Build call graph from call relationship dictionary
    """
    g = nx.DiGraph()
    for k, v in calls.items():
        for dest in v:
            g.add_edge(k, dest)
    return g
