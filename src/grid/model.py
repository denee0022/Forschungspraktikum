import random

import networkx as nx
import numpy as np
from mesa import Model
from typing import Optional

from mesa.space import NetworkGrid
from mesa.time import SimultaneousActivation
from src.grid.citizen import Citizen
from src.grid.roadNetwork import RoadNetwork
from mesa.datacollection import DataCollector


class CityModel(Model):
    def __init__(self, width=6, height=6, n_agents=100, park_fraction=0.1,
                 park_good_fraction=1, park_medium_fraction=0, park_bad_fraction=0,
                 market_fraction=0.1, house_fraction=0.3,
                 work_fraction=0.3,
                 seed: Optional[int] = 42):
        super().__init__()

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        graph = nx.complete_graph(width * height)

        self.road = RoadNetwork(graph)
        self.grid = NetworkGrid(self.road.graph)
        self.schedule = SimultaneousActivation(self)

        all_nodes = list(self.road.graph.nodes())

        #if n_agents > len(all_nodes):
        #    raise ValueError("Mehr Agenten als Knoten!")
        print(all_nodes)
        n_houses = int(len(all_nodes) * house_fraction)
        home_nodes = list(np.random.choice(all_nodes, size=n_houses, replace=False))
        self.homes = set(home_nodes)

        n_workplaces = int(len(all_nodes) * work_fraction)
        available_for_workplaces = list(set(all_nodes) - set(home_nodes))
        workplace_nodes = list(np.random.choice(available_for_workplaces, size=n_workplaces, replace=False))
        self.workplaces = set(workplace_nodes)

        available_for_parks = list(set(all_nodes) - set(home_nodes) - self.workplaces)
        n_parks = max(1, int(len(all_nodes) * park_fraction))
        park_nodes = list(np.random.choice(available_for_parks, size=n_parks, replace=False))
        self.parks = set(park_nodes)

        n_parks_good = max(1, int(n_parks * park_good_fraction))
        n_parks_medium = max(1, int(n_parks * park_medium_fraction))
        n_parks_bad = max(1, int(n_parks * park_bad_fraction))
        print(n_parks_good, n_parks_medium, n_parks_bad)

        self.parks_good = list(np.random.choice(park_nodes, size=n_parks_good, replace=False))
        remaining_after_good = list(set(park_nodes) - set(self.parks_good))
        self.parks_medium = list(np.random.choice(remaining_after_good, size=n_parks_medium, replace=False))
        remaining_after_good_medium = list(set(remaining_after_good) - set(self.parks_medium))
        self.parks_bad = list(np.random.choice(remaining_after_good_medium, size=n_parks_bad, replace=False))
        self.road.set_parks(self.parks, self.parks_good, self.parks_medium, self.parks_bad)

        available_for_markets = list(set(all_nodes) - self.homes - self.workplaces - self.parks)
        n_supermarkets = max(1, int(len(all_nodes) * market_fraction))
        supermarket_nodes = list(np.random.choice(available_for_markets, size=n_supermarkets, replace=False))
        self.supermarkets = set(supermarket_nodes)
        self.road.set_Supermarkets(self.supermarkets)

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

        def goal_to_str(a):
            goal = getattr(a, 'current_goal', None)
            if goal is None:
                return None
            if goal in self.parks_good:
                return 'park_good'
            elif goal in self.parks_medium:
                return 'park_medium'
            elif goal in self.parks_bad:
                return 'park_bad'
            elif goal in self.parks:
                return 'park'
            elif goal in self.supermarkets:
                return 'supermarket'
            elif goal in self.homes:
                return 'home'
            elif goal in self.workplaces:
                return 'workplace'
            else:
                return str(goal)

        self.datacollector = DataCollector(
            model_reporters={
                "Step": lambda m: m.schedule.steps
            },
            agent_reporters={
                "pos": "pos",
                "route": lambda a: getattr(a, 'route', []),
                "current_goal": goal_to_str,
                "current_activity": lambda a: getattr(a, 'current_activity', None),
                "mental_health": lambda a: a.tank_mental_health.level,
                "physical_health": lambda a: a.tank_physical_health.level,
                "leisure": lambda a: a.tank_leisure.level,
                "social_inclusion": lambda a: a.tank_social_inclusion.level,
                "self_determination": lambda a: a.tank_self_determination.level,
                "food": lambda a: a.tank_food.level
            }
        )



    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        all_agents = self.grid.get_all_cell_contents()

        print("=== Agent Status ===")
        for agent in all_agents:
            print(f"Agent {agent.unique_id}: Position {agent.pos}, Aktivität: {agent.current_activity.value}")
            agent.show_tanks()
