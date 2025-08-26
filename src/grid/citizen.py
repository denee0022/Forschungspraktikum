from mesa import Agent

from tank import Tank

class Citizen(Agent):
    def __init__(self, unique_id, model, home, work):
        super().__init__(model)
        self.id = unique_id
        self.home = home
        self.work = work
        self.current_goal = None
        self_route = []
        self.pos = home
        self.time_to_next = 0
        self.state = "to_work"
        self.tank_mental_health = Tank(100, 70)
        self.tank_physical_health = Tank(100, 70)
        self.tank_leisure = Tank(100, 70)
        self.tank_social_inclusion = Tank(100, 70)
        self.tank_food = Tank(100, 70)

    def step(self):
        print()
