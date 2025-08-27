import mesa
from math import dist


class Citizen(mesa.Agent):
    def __init__(self, model, home, schedule, time_budget, preference_weights):
        super().__init__(model)
        self.current_time = 0  # Beginn der Simulation bei 0:00 Uhr
        self.schedule = schedule
        self.current_activity = "home"
        self.destination = home.pos
        self.home = home
        self.time_budget = time_budget
        self.preference_weights = preference_weights
        self.distances = {}
        self.tank = 0 #Test

    def step(self):
        self.current_time = (self.current_time + 1) % 24
        self.choose_activity()
        self.move_towards()

    def choose_activity(self):
        pass  # Überlegen wie man die Aktivität entscheidet

    #Methode in einzelnen Methoden aufteilen
    def move_towards(self):
        old_pos = self.pos
        self.get_place_distances()

        # Schrittgröße (wie weit Agent pro Tick gehen soll)
        step_size = 1.0

        if self.pos == self.destination:
            # Nächstgelegener Ort mit Distanz > 0 finden
            valid_places = [info for info in self.distances.values() if info["distance"] > 0]
            if not valid_places:
                return  # Agent steht auf allen Orten gleichzeitig (sollte nicht passieren)

            nearest = min(valid_places, key=lambda x: x["distance"])
            target_pos = nearest["pos"]

            # Richtung berechnen
            dx = target_pos[0] - self.pos[0]
            dy = target_pos[1] - self.pos[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5

            # Schritt nur, wenn nötig
            if distance > 0:
                move_x = self.pos[0] + (dx / distance) * min(step_size, distance)
                move_y = self.pos[1] + (dy / distance) * min(step_size, distance)
                self.model.space.move_agent(self, (move_x, move_y))

            self.destination = target_pos
            #print(f"Agent {self.unique_id} geht Richtung {nearest['kind']} → {nearest['pos']} ({nearest['distance']:.2f})")
            #print(f"Alte Postion  {old_pos} ändert sich zur folgenden Position {self.pos}")
        else:

            # Richtung berechnen
            dx = self.destination[0] - self.pos[0]
            dy = self.destination[1] - self.pos[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5 #euklidischer Abstand

            # Schritt nur, wenn nötig
            if distance > 0:
                move_x = self.pos[0] + (dx / distance) * min(step_size, distance)
                move_y = self.pos[1] + (dy / distance) * min(step_size, distance)
                self.model.space.move_agent(self, (move_x, move_y))

    def get_place_distances(self):
        for place in self.model.places:
            self.distances[place.unique_id] = {
                "kind": place.kind,
                "pos": place.pos,
                "distance": dist(self.pos, place.pos)
            }
        self.distances[self.home.unique_id] = {
            "kind": self.home.kind,
            "pos": self.home.pos,
            "distance": dist(self.pos, self.home.pos)
        }

