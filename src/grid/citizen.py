from mesa import Agent

from tank import Tank
from action import Action
from constants import Activity
from daily_schedule import DailySchedule
import random
import numpy as np


class Citizen(Agent):
    def __init__(self, unique_id, model, home, work):
        # hier nochmal schauen. Bei mesa version 2.3.2 scheint es 2 Parameter zu brauchen
        super().__init__(model)
        self.id = unique_id
        self.home = home
        self.work = work
        self.current_goal = work
        self.route = []
        self.pos = home
        self.time_to_next = 0
        self.current_activity = Activity.SLEEPING

        np.random.seed(42)  # random Seed, um Tanks zufällig zu füllen
        self.tank_mental_health = Tank(100, np.random.randint(20, 100), np.random.randint(5, 30))
        self.tank_physical_health = Tank(100, np.random.randint(20, 100), np.random.randint(5, 30))
        self.tank_leisure = Tank(100, np.random.randint(20, 100), np.random.randint(5, 30))
        self.tank_social_inclusion = Tank(100, np.random.randint(20, 100), np.random.randint(5, 30))
        self.tank_self_determination = Tank(100, np.random.randint(20, 100), np.random.randint(5, 30))
        self.tank_food = Tank(100, np.random.randint(20, 100), np.random.randint(5, 30))
        self.action = Action()
        self.daily_schedule = DailySchedule()

    def step(self):
        current_step = self.model.schedule.steps if hasattr(self.model.schedule, 'steps') else 0
        scheduled_activity = self.daily_schedule.get_activity_for_step(current_step)
        if scheduled_activity.value != self.current_activity.value:
            self.current_activity = scheduled_activity
            print(f"Citizen {self.unique_id}: Neue Aktivität: {self.current_activity} (Step {current_step})")

            if self.current_activity.value == Activity.WORKING.value:
                self.current_goal = self.work
                print("Komme ich hier rein?")
            elif self.current_activity.value == Activity.LEISURE.value:
                self.current_goal = self.choose_leisure_location()
            else:  # SLEEPING
                self.current_goal = self.home
            print(f"Agent {self.unique_id} Position: {self.pos}, Ziel: {self.current_goal}")

            start = self.pos
            goal = self.current_goal
            self.route = self.model.road.shortest_path_sparse(start, goal)

            for step in self.route:
                if step in self.model.parks:
                    self.action.path_UGS(self)
                else:
                    self.action.path_street(self)

            print(f"Kürzeste Route für Agent {self.unique_id}: {self.route}")
            self.model.grid.move_agent(self, goal)
            self.pos = goal
            self.route = []
            if self.pos == self.current_goal:
                self.execute_current_activity()

    def choose_leisure_location(self):
        return random.choice(list(self.model.parks))

    def execute_current_activity(self):
        if self.current_activity == Activity.SLEEPING:
            self.action.sleeping(self)
        elif self.current_activity == Activity.WORKING:
            self.action.working(self)
        elif self.current_activity == Activity.LEISURE:
            # Je nach Ort verschiedene Freizeitaktivitäten
            if self.pos in getattr(self.model, 'parks', set()):
                self.action.freetime_UGS(self)
            else:
                self.action.freetime_home(self)

    def show_tanks(self):
        print(f"Mental-Health:  {self.tank_mental_health.level}; "
              f"Physical-Health: {self.tank_physical_health.level}; "
              f"Leisure-Tank: {self.tank_leisure.level}; "
              f"social-inclusion: {self.tank_social_inclusion.level}; "
              f"self-determination: {self.tank_self_determination.level}; "
              )
