from collections import defaultdict
from typing import Any
from .. import dsl
import gravis as gv

#--------------------------------------------------
# Graph
#--------------------------------------------------

class Compute:
    def __init__(self, graph:'Graph'):
        self._graph = graph
        self._lib = getattr(self._graph.model.rel, self._graph._lib_ref())

    def degree(self, node, weight=None):
        if not weight:
            return self._lib.degree(node)
        return self._lib.weighted_degree(node)

    def pagerank(self, node):
        return self._lib.pagerank(node)

    def betweenness_centrality(self, node):
        return self._lib.betweenness_centrality(node)

    def degree_centrality(self, node):
        return self._lib.degree_centrality(node)

    def label_propagation(self, node):
        return self._lib.label_propagation(node)

    def weakly_connected_component(self, node):
        return self._lib.weakly_connected_component(node)

class Nodes:
    def __init__(self, graph:'Graph'):
        self._graph = graph
        self._type = dsl.RawRelation(self._graph.model, f"graph{self._graph.id}_nodes", 1)
        self._props = {}

    def _prop(self, name:str):
        if name not in self._props:
            self._props[name] = dsl.RawRelation(self._graph.model, f"graph{self._graph.id}_node_{name}", 2)
        return self._props[name]

    def extend(self, type:dsl.Type, **kwargs):
        with self._graph.model.rule():
            t = type()
            self.add(t, **kwargs)

    def add(self, node, **kwargs):
        self._type.add(node)
        for k, v in kwargs.items():
            if isinstance(v, dsl.Property):
                v = getattr(node, v._name)
            self._prop(k).add(node, v)

    def __getattribute__(self, __name: str) -> Any:
        if __name in ["add", "extend"] or __name.startswith("_"):
            return super().__getattribute__(__name)
        return self._props[__name]

class Edges:
    def __init__(self, graph:'Graph'):
        self._graph = graph
        self._type = dsl.RawRelation(self._graph.model, f"graph{self._graph.id}_edges", 2)
        self._props = {}

    def _prop(self, name:str):
        if name not in self._props:
            self._props[name] = dsl.RawRelation(self._graph.model, f"graph{self._graph.id}_edge_{name}", 3)
        return self._props[name]

    def extend(self, prop:'dsl.Property|Edge', **kwargs):
        type = prop._provider
        with self._graph.model.rule():
            t = type()
            self.add(t, getattr(t, prop._name), **kwargs)

    def add(self, from_:Any, to:Any, **kwargs):
        self._type.add(from_, to)
        for k, v in kwargs.items():
            self._prop(k).add(from_, to, v)

    def __getattribute__(self, __name: str) -> Any:
        if __name in ["add", "extend"] or __name.startswith("_"):
            return super().__getattribute__(__name)
        return self._props[__name]

class Graph:
    def __init__(self, model:dsl.Graph, undirected=False):
        self.model = model
        self.id = dsl.next_id()
        self.compute = Compute(self)
        self.nodes = Nodes(self)
        self.edges = Edges(self)
        self.undirected = undirected
        self._last_fetch = None

        graph_type = "undirected_graph" if undirected else "directed_graph"
        self.model.install_raw(f"""
        bound {self.edges._type._name}
        def {self._graph_ref()} = {graph_type}[{self.edges._type._name}]
        @inline
        def {self._lib_ref()} = rel:graphlib[{self._graph_ref()}]
        """)

    def _graph_ref(self):
        return f"graph{self.id}"

    def _lib_ref(self):
        return f"graphlib{self.id}"

    def visualize(self, three=False, **kwargs):
        data = self._last_fetch
        if not data:
            data = self.fetch()
        def prepare_metadata(info):
            metadata = {}
            allowed_gjgf_node_keys = [
                "color",
                "opacity",
                "size",
                "shape",
                "border_color",
                "border_size",
                "label_color",
                "label_size",
                "hover",
                "click",
                "image",
                "x",
                "y",
                "z",
            ]
            hover_text = "\n".join([f"{k}: {v}" for (k,v) in info.items()
                                    if k not in allowed_gjgf_node_keys + ["label"]])
            for k in allowed_gjgf_node_keys:
                if k in info:
                    metadata[k] = info[k]
            if hover_text:
                metadata["hover"] = "\n".join([metadata["hover"] or "", hover_text])
            return metadata
        graph1 = {
            "graph": {
                "directed": not self.undirected,
                "metadata": {
                    "arrow_size": 4,
                    "edge_size": 1,
                    "edge_label_size": 10,
                    "edge_label_color": "#E1856C",
                    "edge_color": "#E1856C",
                    "node_size": 10,
                    "node_color": "#474B77",
                    "node_label_color": "#474B77",
                    "node_label_size": 10,
                },
                "nodes": {
                    node_id: {
                        **({"label": info["label"]} if "label" in info else {}),
                        "metadata": prepare_metadata(info),
                    }
                    for (node_id, info) in data["nodes"].items()
                },
                "edges": [
                    {"source": source, "target": target, "metadata": info}
                    for ((source, target), info) in data["edges"].items()
                ],
            }
        }

        vis = gv.vis if not three else gv.three
        fig = vis(graph1, edge_label_data_source='label', node_label_data_source='label', edge_curvature=0.4, **kwargs)
        return fig

    def fetch(self):
        code = []
        code.append(f"def output:nodes(n) = {self.nodes._type._name}(n)")
        for name, prop in self.nodes._props.items():
            code.append(f"def output:nodes:{name}(n, v) = {prop._name}(n, v)")
        code.append(f"def output:edges(a,b) = {self.edges._type._name}(a,b)")
        for name, prop in self.edges._props.items():
            code.append(f"def output:edges:{name}(a,b,v) = {prop._name}(a,b,v)")

        output = {"nodes": defaultdict(dict), "edges": defaultdict(dict)}
        results = self.model.exec_raw("\n".join(code), raw_results=True)
        for set in results.results:
            path = [v[1:] for v in set["relationId"].split("/")[2:] if v[0] == ":"]
            if path[0] not in ["nodes", "edges"]:
                continue
            cur = output[path[0]]
            if path[0] == "nodes":
                if len(path) == 1:
                    for (n,) in set["table"].itertuples(index=False):
                        cur[n]
                else:
                    for (n,v) in set["table"].itertuples(index=False):
                        cur[n][path[1]] = v
            elif path[0] == "edges":
                if len(path) == 1:
                    for (a,b) in set["table"].itertuples(index=False):
                        cur[(a,b)]
                else:
                    for (a,b,v) in set["table"].itertuples(index=False):
                        cur[(a,b)][path[1]] = v
            else:
                raise Exception(f"Unexpected path: {path}")
        self._last_fetch = output
        return output

#--------------------------------------------------
# Edge
#--------------------------------------------------

class Edge:
    def __init__(self, type:Any, from_:Any, to:Any):
        # raise NotImplementedError()
        pass

    def __call__(self, *args, **kwargs):
        return self

    def __getattribute__(self, __name: str) -> Any:
        pass

    def __getitem__(self, item):
        return self

#--------------------------------------------------
# Path
#--------------------------------------------------

class Path:
    def __init__(self, *args):
        self.edges = []
        self.nodes = []
        pass

    def __getitem__(self, item):
        return self
