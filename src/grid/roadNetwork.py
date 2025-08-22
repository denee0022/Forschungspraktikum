import math
from typing import List

import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra


class RoadNetwork:

    def __init__(self, graph: nx.Graph):
        self.graph = graph

        self.index_of = {n: i for i, n in enumerate(self.graph.nodes)}
        self.node_of = {i: n for n, i in self.index_of.items()}
        self.n = len(self.index_of)

        # Edge defaults
        for u, v, data in self.graph.edges(data=True):
            data.setdefault("length", 1.0)
            data.setdefault("base_time", data["length"] / 1.0)
            data.setdefault("travel_time", data["base_time"])

        self._build_sparse()

    def _build_sparse(self):
        rows, cols, weights = [], [], []
        for u, v, d in self.graph.edges(data=True):
            i, j = self.index_of[u], self.index_of[v]
            tt = d.get("travel_time", 1.0)
            for (r, c) in [(i, j), (j, i)]:
                rows.append(r)
                cols.append(c)
                weights.append(tt)
        self.sparse = csr_matrix((weights, (rows, cols)), shape=(self.n, self.n))

    def update_travel_times(self):
        for u, v, d in self.graph.edges(data=True):
            d["travel_time"] = d.get("base_time", 1.0)
        self._build_sparse()

    def shortest_path_sparse(self, src: int, dst: int) -> List[int]:
        """Dijkstra auf Sparse-Matrix."""
        dist_matrix, predecessors = dijkstra(csgraph=self.sparse, directed=False, indices=src, return_predecessors=True)
        if np.isinf(dist_matrix[dst]):
            return []
        # Pfad rekonstruieren
        path = []
        i = dst
        while i != src:
            path.append(i)
            i = predecessors[i]
            if i == -9999:  # kein Pfad
                return []
        path.append(src)
        path.reverse()
        return path

    def edge_travel_time(self, a: int, b: int) -> float:
        u, v = self.node_of[a], self.node_of[b]
        if self.graph.has_edge(u, v):
            return self.graph[u][v]["travel_time"]
        return math.inf
