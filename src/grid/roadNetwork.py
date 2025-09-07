import math
from typing import List, Tuple

import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix, csgraph
from scipy.sparse.csgraph import dijkstra
from constants import PreferenceType
import random

np.random.seed(42)


class RoadNetwork:

    def __init__(self, graph: nx.Graph):
        self.graph = graph

        self.index_of = {n: i for i, n in enumerate(self.graph.nodes)}
        self.node_of = {i: n for n, i in self.index_of.items()}
        self.n = len(self.index_of)

        self.supermarkets = set()
        self.parks = set()
        self.park_good = set()
        self.park_medium = set()
        self.park_bad = set()

        self.targets = set()
        self.park_greenscores = {}

        # Edge defaults
        for u, v, data in self.graph.edges(data=True):
            """
            data.setdefault("length", 1.0)
            data.setdefault("base_time", data["length"] / 1.0)
            data.setdefault("travel_time", data["base_time"])
            """
            time = random.uniform(0.5, 3.0)  # zufällige Länge zwischen 0.5 und 2.0
            data["travel_time"] = time
            data["greenscore"] = 0
        self._build_sparse()

    def set_parks(self, parks, park_good_quality, park_medium_quality, park_bad_quality):
        self.parks = parks
        self.park_good = park_good_quality
        self.park_medium = park_medium_quality
        self.park_bad = park_bad_quality

        for park_node in self.park_good:
            self.graph.nodes[park_node]['greenscore'] = np.random.randint(66, 100)

        for park_node in self.park_medium:
            self.graph.nodes[park_node]['greenscore'] = np.random.randint(33, 65)

        for park_node in self.park_bad:
            self.graph.nodes[park_node]['greenscore'] = np.random.randint(1, 32)

        self.calculate_road_greenscores()

    def calculate_road_greenscores(self, max_distance=1):
        park_influences = {}
        all_park_types = [
            self.park_good,
            self.park_medium,
            self.park_bad
        ]

        for park_set in all_park_types:
            for park_node in park_set:
                park_score = self.graph.nodes[park_node].get('greenscore', 0)
                distances = nx.single_source_shortest_path_length(
                    self.graph, park_node, cutoff=max_distance
                )
                for node, distance in distances.items():
                    if node not in park_influences:
                        park_influences[node] = []
                    park_influences[node].append((park_score, distance))

        for u, v, data in self.graph.edges(data=True):
            base_score = data.get("greenscore", 0)
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

        self._build_sparse()
        self.print_matrices()

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

    def edge_travel_time(self, a, b, matrix=None) -> float:
        if matrix is None:
            matrix = self.sparse_travel_time
        if 0 <= a < self.n and 0 <= b < self.n:
            return float(matrix[a, b])
        return math.inf

    def edge_greenscore(self, a: int, b: int, matrix=None) -> float:
        if matrix is None:
            matrix = self.sparse_greenscore
        if 0 <= a < self.n and 0 <= b < self.n:
            return float(matrix[a, b])
        return 0.0

    # hier wird nur nach der TravelTime geschaut
    def shortest_path_sparse(self, src: int, dst: int, sparse_matrix: csgraph) -> List[int]:
        """Dijkstra auf Sparse-Matrix."""
        dist_matrix, predecessors = dijkstra(csgraph=sparse_matrix, directed=False,
                                             indices=src, return_predecessors=True)

        if np.isinf(dist_matrix[dst]):
            return []
        # Pfad rekonstruieren
        path = []
        i = dst
        while i != src:
            path.append(int(i))
            i = predecessors[i]
            if i == -9999:  # kein Pfad
                return []
        path.append(int(src))
        path.reverse()
        #for i in range(len(path) - 1):
        #print(
        #    f"Greenscore zwischen Knoten {path[i]} und {path[i + 1]} ist: {self.edge_greenscore(path[i], path[i + 1])}")
        return path

    def calculate_edge_cost_with_preferences(self, a, b, route_weight_dict):
        base_cost = self.edge_travel_time(a, b)
        greenscore = self.edge_greenscore(a, b)

        efficiency_weight = route_weight_dict.get(PreferenceType.EFFICIENCY, 0.5)
        green_weight = route_weight_dict.get(PreferenceType.GREEN_ENVIRONMENT, 0.5)

        efficiency_cost = base_cost * efficiency_weight
        normalized_greenscore = greenscore / 100.0
        green_reduction = normalized_greenscore * green_weight
        final_cost = efficiency_cost - green_reduction

        return max(0.1, final_cost)

    def build_preference_sparse_matrix(self, route_weights_dict):
        rows, cols, adjusted_costs = [], [], []

        for u, v, d in self.graph.edges(data=True):
            i, j = self.index_of[u], self.index_of[v]
            adjusted_cost = self.calculate_edge_cost_with_preferences(u, v, route_weights_dict)
            for (r, c) in [(i, j), (j, i)]:
                rows.append(r)
                cols.append(c)
                adjusted_costs.append(adjusted_cost)
        return csr_matrix((adjusted_costs, (rows, cols)), shape=(self.n, self.n))

    def best_path(self, src: int, dst: int, route_weights_dict, home=None, locations=None, tank_weights=None) -> List[
        int]:
        preference_matrix = self.build_preference_sparse_matrix(route_weights_dict)
        if locations is not None and len(locations) > 0:
            best_score = float('inf')
            best_route = None
            best_goal = None
            best_loc = None
            for loc in locations:
                if loc == 'supermarket':
                    self.targets = self.supermarkets
                elif loc == 'park':
                    self.targets = self.parks
                elif loc == 'home':
                    self.targets = [home]
                for target in self.targets:
                    route = self.shortest_path_sparse(src, target, preference_matrix)
                    cost = sum(self.edge_travel_time(route[i], route[i + 1], matrix=preference_matrix) for i in
                               range(len(route) - 1))
                    # Tankpräferenz einbeziehen
                    if tank_weights is not None:
                        if target in self.parks:
                            tank_types = {PreferenceType.PHYSICAL_HEALTH, PreferenceType.SOCIAL_INCLUSION}
                        elif target in self.supermarkets:
                            tank_types = {PreferenceType.FOOD}
                        elif target == home:
                            tank_types = {PreferenceType.MENTAL_HEALTH}
                        else:
                            tank_types = set()
                        for tank_type in tank_types:
                            cost -= tank_weights.get(tank_type, 0)
                            """print(f"Kosten: {cost}")
                            print(f"Route: {route}")
                            print(f"Target: {target}")
                            print(f"Loc: {loc}")"""
                            if cost < best_score:
                                best_score = cost
                                best_route = route
                                best_goal = target
                                best_loc = loc
                                """print(f"Beste Score: {best_score}")
                                print(f"Beste Route: {best_route}")
                                print(f"Beste Goal: {best_goal}")
                                print(f"Beste Loc: {best_loc}")"""
            return best_route, best_goal, best_loc
        else:
            return self.shortest_path_sparse(src, dst, preference_matrix)

    def set_Supermarkets(self, supermarkets):
        self.supermarkets = supermarkets

    def get_greenscore_park(self, park_node):
        if park_node in self.park_greenscores:
            return self.park_greenscores[park_node]
        else:
            return 0.0

    def print_matrices(self, route_weights_dict=None):
        import numpy as np
        print("Greenscore-Matrix:")
        greenscore_matrix = self.sparse_greenscore.toarray()
        print(np.round(greenscore_matrix, 10))

        print("\nTravelTime-Matrix:")
        traveltime_matrix = self.sparse_travel_time.toarray()
        print(np.round(traveltime_matrix, 10))

        if route_weights_dict is not None:
            print("\nPräferenz-Matrix (kombiniert):")
            pref_matrix = self.build_preference_sparse_matrix(route_weights_dict).toarray()
            print(np.round(pref_matrix, 10))
        else:
            print("\nKeine Präferenz-Matrix berechnet (route_weights_dict=None)")
