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
    def __init__(self, width=6, height=6, n_agents=100, park_fraction=0.1, market_fraction=0.3, house_fraction=0.5,
                 work_fraction=0.3, seed: Optional[int] = 42):
        super().__init__()

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        graph = nx.grid_2d_graph(width, height)
        mapping = {xy: i for i, xy in enumerate(graph.nodes())}
        graph = nx.relabel_nodes(graph, mapping)

        self.road = RoadNetwork(graph)
        self.grid = NetworkGrid(self.road.graph)
        self.schedule = SimultaneousActivation(self)  #Agenten handeln gleichzeitig

        all_nodes = list(self.road.graph.nodes())

        if n_agents > len(all_nodes):
            raise ValueError("Mehr Agenten als Knoten!")

        n_houses = int(n_agents * house_fraction)
        home_nodes = list(np.random.choice(all_nodes, size=n_houses, replace=False))
        self.homes = set(home_nodes)

        n_workplaces = int(n_agents * work_fraction)
        available_for_workplaces = list(set(all_nodes) - set(home_nodes))
        workplace_nodes = list(np.random.choice(available_for_workplaces, size=n_workplaces, replace=False))
        self.workplaces = set(workplace_nodes)

        available_for_parks = list(set(all_nodes) - set(home_nodes) - self.workplaces)
        n_parks = max(1, int(len(all_nodes) * park_fraction))
        park_nodes = list(np.random.choice(available_for_parks, size=n_parks, replace=False))
        self.parks = set(park_nodes)

        available_for_markets = list(set(all_nodes) - self.homes - self.workplaces - self.parks)
        n_supermarkets = max(1, int(len(all_nodes) * market_fraction))
        supermarket_nodes = list(np.random.choice(available_for_markets, size=n_supermarkets, replace=False))
        self.supermarkets = set(supermarket_nodes)

        citizens = []
        assigned_homes = []
        for i, home in enumerate(home_nodes):
            assigned_homes.append(home)

        assigned_workplaces = []
        for i, workplace in enumerate(workplace_nodes):
            assigned_workplaces.append(workplace)

        min_agents = max(len(assigned_homes), len(assigned_workplaces))
        agents_assigned = 0
        for i in range(min_agents):
            home = assigned_homes[i % len(assigned_homes)]
            work = assigned_workplaces[i % len(assigned_workplaces)]
            citizen = Citizen(i, self, home, work)
            citizens.append(citizen)
            self.grid.place_agent(citizen, home)
            self.schedule.add(citizen)
            agents_assigned += 1

        for i in range(agents_assigned, n_agents):
            home = int(np.random.choice(home_nodes))
            work = int(np.random.choice(workplace_nodes))
            citizen = Citizen(i, self, home, work)
            citizens.append(citizen)
            self.grid.place_agent(citizen, home)
            self.schedule.add(citizen)

    def step(self):
        self.schedule.step()
        all_agents = self.grid.get_all_cell_contents()

        print("=== Agent Status ===")
        for agent in all_agents:
            print(f"Agent {agent.unique_id}: Position {agent.pos}, Aktivität: {agent.current_activity.value}")
            agent.show_Tanks()
