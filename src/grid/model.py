import random

import networkx as nx
import numpy as np
from mesa import Model
from typing import Optional

from mesa.space import NetworkGrid
from mesa.time import SimultaneousActivation

from src.grid.citizen import Citizen
from src.grid.roadNetwork import RoadNetwork


class CityModel(Model):
    def __init__(self, width=6, height=6, n_agents=100, park_fraction=0.1, market_fraction=0.3,
                 seed: Optional[int] = 42):
        super().__init__()
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        graph = nx.grid_2d_graph(width, height)
        mapping = {xy: i for i, xy in enumerate(graph.nodes())}
        graph = nx.relabel_nodes(graph, mapping)

        for u, v in graph.edges():
            graph[u][v]["length"] = 1.0
            graph[u][v]["base_time"] = 1.0  # hier überlegen ob man random length und basetime macht

        self.road = RoadNetwork(graph)
        self.grid = NetworkGrid(self.road.graph)
        self.schedule = SimultaneousActivation(self)  #Agenten handeln gleichzeitig

        all_nodes = list(self.road.graph.nodes())

        if n_agents > len(all_nodes):
            raise ValueError("Mehr Agenten als Knoten!")
        home_nodes = np.random.choice(all_nodes, size=n_agents, replace=False)

        available_for_parks = list(set(all_nodes) - set(home_nodes))
        n_parks = max(1, int(len(all_nodes) * park_fraction))
        self.parks = set(np.random.choice(available_for_parks, size=n_parks, replace=False))

        available_for_markets = list(set(all_nodes) - set(home_nodes) - self.parks)
        n_supermarkets = max(1, int(len(all_nodes) * market_fraction))
        self.supermarkets = set(np.random.choice(available_for_markets, size=n_supermarkets, replace=False))

        for i, home in enumerate(home_nodes):
            # Work-Knoten kann optional Home-Knoten ausschließen
            work = int(np.random.choice(list(set(all_nodes) - {home})))
            a = Citizen(i, self, home, work)
            self.grid.place_agent(a, home)
            self.schedule.add(a)

        def step(self):
            self.schedule.step()
















