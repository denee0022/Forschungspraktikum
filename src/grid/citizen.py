from mesa import Agent

from tank import Tank

class Citizen(Agent):
    def __init__(self, unique_id, model, home, work):
        super().__init__(model)
        self.id = unique_id
        self.home = home
        self.work = work
        self.current_goal = work
        self.route = []
        self.pos = home
        self.time_to_next = 0
        self.state = "to_work"
        self.tank_mental_health = Tank(100, 70)
        self.tank_physical_health = Tank(100, 70)
        self.tank_leisure = Tank(100, 70)
        self.tank_social_inclusion = Tank(100, 70)
        self.tank_food = Tank(100, 70)

    def step(self):
        if not self.route:
            start = self.pos
            goal = self.current_goal

            self.route = self.model.road.shortest_path_sparse(start, goal)
            print(f"Kürzeste Route für Agent {self.unique_id}: {self.route}")
            self.pos = goal
            self.model.grid.place_agent(self, self.pos)
            print(f"Agent {self.unique_id} befindet sich gerade in:  {self.pos}")
        if len(self.route) <= 1:
            if self.state == "to_work":
                self.state = "to_home"
                self.current_goal = self.home
            else:
                self.state = "to_work"
                self.current_goal = self.work
            self.route = []

