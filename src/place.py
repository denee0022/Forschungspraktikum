import mesa


class Place(mesa.Agent):
    def __init__(self, model, kind, pos):
        super().__init__(model)
        self.kind = kind  # "home", "work", "park", "store"

    def step(self):
        pass
