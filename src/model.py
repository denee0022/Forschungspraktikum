import mesa
import random
from agent import Citizen
from place import Place


class CityModel(mesa.Model):
    def __init__(self, population):
        super().__init__()
        self.space = mesa.space.ContinuousSpace(100, 100, True)
        self.places = []

        # Orte erzeugen
        self.add_place("work", (80, 80))
        self.add_place("park", (50, 50))
        self.add_place("store", (30, 80))
        # Citizens erzeugen
        for i in range(population):
            home_pos = (random.uniform(10, 40), random.uniform(10, 40))
            home = self.add_place("home", home_pos)
            schedule = {
                8: "work",
                17: "store",
                19: "park",
                21: "home"
            }
            citizen = Citizen(self, home, schedule, 0, 0)
            self.space.place_agent(citizen, home_pos)

    def add_place(self, kind, pos):
        place = Place(self, kind, pos)
        self.space.place_agent(place, pos)
        if kind != "home":
            self.places.append(place)
        return place

    def step(self):
        for agent in self.agents:
            if isinstance(agent, Citizen):
                agent.step()
               # print(agent.unique_id)
        #for place in self.places:
            #print(place.kind)