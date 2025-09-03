import math
from typing import List, Tuple

import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
import random


class RoadNetwork:

    def __init__(self, graph: nx.Graph):
        self.graph = graph

        self.index_of = {n: i for i, n in enumerate(self.graph.nodes)}
        self.node_of = {i: n for n, i in self.index_of.items()}
        self.n = len(self.index_of)

        self.parks = set()
        self.park_greenscores = {}

        # Edge defaults
        for u, v, data in self.graph.edges(data=True):
            """
            data.setdefault("length", 1.0)
            data.setdefault("base_time", data["length"] / 1.0)
            data.setdefault("travel_time", data["base_time"])
            """
            length = random.uniform(0.5, 2.0)  # zufällige Länge zwischen 0.5 und 2.0
            data["travel_time"] = length
            data["greenscore"] = random.uniform(0, 50)
        self._build_sparse()

    def set_parks(self, park_nodes):
        self.parks = park_nodes
        self.park_greenscores = {}

        for park_node in self.parks:
            self.park_greenscores[park_node] = random.uniform(20, 100)

        self.calculate_road_greenscores()
        self._build_sparse()

    def calculate_road_greenscores(self, max_distance=3):
        park_influences = {}

        for park_node in self.parks:
            distances = nx.single_source_shortest_path_length(
                self.graph, park_node, cutoff=max_distance
            )

            park_score = self.park_greenscores[park_node]

            for node, distance in distances.items():
                if node not in park_influences:
                    park_influences[node] = []
                park_influences[node].append((park_score, distance))

        for u, v, data in self.graph.edges(data=True):
            base_score = data.get("greenscore", 30)

            total_influence = 0
            node_count = 0

            for node in [u, v]:
                if node in park_influences:
                    for park_score, distance in park_influences[node]:
                        if distance <= max_distance:
                            influence_strength = max(0, 1 - (distance / max_distance))
                            total_influence += park_score * influence_strength * 0.01
                            node_count += 1

            avg_influence = total_influence / max(1, node_count)
            final_score = min(100, base_score + avg_influence * 25)

            data["greenscore"] = max(0, final_score)

    def _build_sparse(self):
        rows, cols, travel_times, greenscores = [], [], [], []
        for u, v, d in self.graph.edges(data=True):
            i, j = self.index_of[u], self.index_of[v]
            tt = d.get("travel_time", 1.0)
            gs = d.get("greenscore", 30)
            for (r, c) in [(i, j), (j, i)]:
                rows.append(r)
                cols.append(c)
                travel_times.append(tt)
                greenscores.append(gs)
        self.sparse_travel_time = csr_matrix((travel_times, (rows, cols)), shape=(self.n, self.n))
        self.sparse_greenscore = csr_matrix((greenscores, (rows, cols)), shape=(self.n, self.n))

    def get_edge_data(self, a: int, b: int) -> Tuple[float, float]:
        if 0 <= a < self.n and 0 <= b < self.n:
            travel_time = self.sparse_travel_time[a, b]
            greenscore = self.sparse_greenscore[a, b]
            return float(travel_time), float(greenscore)
        return math.inf, 0.0

    def edge_travel_time(self, a: int, b: int) -> float:
        if 0 <= a < self.n and 0 <= b < self.n:
            return float(self.sparse_travel_time[a, b])
        return math.inf

    def edge_greenscore(self, a: int, b: int) -> float:
        if 0 <= a < self.n and 0 <= b < self.n:
            return float(self.sparse_greenscore[a, b])
        return 0.0

    # hier wird nur nach der TravelTime geschaut
    def shortest_path_sparse(self, src: int, dst: int) -> List[int]:
        """Dijkstra auf Sparse-Matrix."""
        dist_matrix, predecessors = dijkstra(csgraph=self.sparse_travel_time, directed=False,
                                             indices=src, return_predecessors=True)
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
        for i in range(len(path) - 1):
            print(f"Greenscore zwischen Knoten {path[i]} und {path[i + 1]} ist: {self.edge_greenscore(path[i],path[i+1])}")
        return path