from mesa import Agent


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

    def step(self):
        print()
