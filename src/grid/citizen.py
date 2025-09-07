from matplotlib._mathtext import Accent
from mesa import Agent

from tank import Tank
from action import Action
from constants import Activity, PreferenceType
from daily_schedule import DailySchedule
import random
import numpy as np
from citizien_prefence import CitizienPreferences

class Citizen(Agent):
    def __init__(self, unique_id, model, home, work, citizien_tank_preference=None, citizien_route_preference=None):
        # hier nochmal schauen. Bei mesa version 2.3.2 scheint es 2 Parameter zu brauchen
        super().__init__(model)
        self.id = unique_id
        self.home = home
        self.work = work
        self.current_goal = work
        self.route = []
        self.pos = home
        self.location = "home"
        self.time_to_next = 0
        self.current_activity = Activity.SLEEPING
        #Create preferences
        self.preferences = CitizienPreferences(citizien_tank_preference, citizien_route_preference)
        self.bestPref_tank = self.preferences.get_highest_tank_preference_type()
        self.bestPref_route = self.preferences.get_highest_route_preference_type()
        #Watertank for every need
        self.tank_mental_health = Tank(100, np.random.randint(70, 100), np.random.randint(20, 30))
        self.tank_physical_health = Tank(100, np.random.randint(70, 100), np.random.randint(20, 30))
        self.tank_leisure = Tank(100, np.random.randint(70, 100), np.random.randint(20, 30))
        self.tank_social_inclusion = Tank(100, np.random.randint(70, 100), np.random.randint(20, 30))
        self.tank_self_determination = Tank(100, np.random.randint(70, 100), np.random.randint(20, 30))
        self.tank_food = Tank(100, np.random.randint(70, 100), np.random.randint(20, 30))

        self.life_quality = 0
        self.action = Action()
        self.daily_schedule = DailySchedule()

    def step(self):
        #loc = ""
        current_step = self.model.schedule.steps if hasattr(self.model.schedule, 'steps') else 0
        scheduled_activity = self.daily_schedule.get_activity_for_step(current_step)
        self.route = []
        if (scheduled_activity.value != self.current_activity.value or
                self.current_activity.value == Activity.LEISURE.value):
            start = self.pos
            route_weigths = self.preferences.route_weights
            self.current_activity = scheduled_activity
            #Pathfinding for Working
            if self.current_activity.value == Activity.WORKING.value:
                self.current_goal = self.work
                self.route = self.model.road.best_path(start, self.current_goal, route_weigths)
                self.location = "work"
            #Pathfinding for Leisure Period
            elif self.current_activity.value == Activity.LEISURE.value:
                locations = self.choose_leisure_location()
                tank_weights = self.preferences.tank_weights
                self.route, self.current_goal, self.location = self.model.road.best_path(start, self.current_goal,
                                                                                         route_weigths,
                                                                                         self.home,
                                                                                         locations, tank_weights)
            #Path finding for Sleeping (going home)
            else:
                self.current_goal = self.home
                self.current_activity = Activity.SLEEPING
                self.route = self.model.road.best_path(start, self.current_goal, route_weigths)
                #print(f"Kürzeste Route für Agent {self.unique_id}: {self.route}")
                self.location = "home"
            #postive effect if going through a park
            for node in self.route:
                if node in self.model.parks and (len(self.route) != 1):
                    self.action.path_UGS(self, self.model.road.get_greenscore_park(node))
                else:
                    self.action.path_street(self)
            self.model.grid.move_agent(self, self.current_goal)
            self.pos = self.current_goal
        self.execute_current_activity(self.location)

    #choose the possible activites according to the need(tanks under threshold)
    def choose_leisure_location(self):
        tank_map = {
            'mental_health': (self.tank_mental_health, PreferenceType.MENTAL_HEALTH),
            'physical_health': (self.tank_physical_health, PreferenceType.PHYSICAL_HEALTH),
            'leisure': (self.tank_leisure, PreferenceType.LEISURE),
            'social_inclusion': (self.tank_social_inclusion, PreferenceType.SOCIAL_INCLUSION),
            'self_determination': (self.tank_self_determination, PreferenceType.SELF_DETERMINATION),
            'food': (self.tank_food, PreferenceType.FOOD)
        }

        tank_levels = self.get_tank_levels_dict()
        under_threshold = []
        for name, (tank, pref_type) in tank_map.items():
            if tank_levels[name] < (tank.threshold / tank.capacity):
                #print(
                 #   f"Tank-Name: {name}: Tank-Level: {tank_levels[name]}, Tank-Threshold: {tank.threshold / tank.capacity}")
                under_threshold.append((name, pref_type))

        if not under_threshold:
            # If no tank is under the threshold the citizen goes home
            return self.best_location_for_tanks(['mental_health'])
        #if len = 1 so just one location else more locations for path finding
        if len(under_threshold) == 1:
            best = max(
                tank_map.items(),
                key=lambda x: self.preferences.get_tank_weight(x[1][1])
            )
            return self.best_location_for_tanks([best[0]])
        else:
            tanks = [name for name, _ in under_threshold]
            #print(f"Leisure_location: {self.best_location_for_tanks(tanks)}")
            return self.best_location_for_tanks(tanks)

    #execute actions depending one the planed activity
    def execute_current_activity(self, location):
        #print(f"location: {location}")
        if self.current_activity == Activity.SLEEPING:
            self.action.sleeping(self)
        elif self.current_activity == Activity.WORKING:
            self.action.working(self)
        elif self.current_activity == Activity.LEISURE:
            # Je nach Ort verschiedene Freizeitaktivitäten
            if location == "park":
                park = self.route[-1]
                self.action.freetime_UGS(self, self.model.road.get_greenscore_park(park))
            elif location == "home":
                #self.pos in getattr(self.model, 'home', set()):
                #print(f"Agent {self.unique_id} geht nach Hause")
                self.action.freetime_home(self)
            else:
                self.action.eating(self)
                #print(f"Agent {self.unique_id} geht zum Supermarkt")

    def get_tank_levels_dict(self):
        return {
            'mental_health': self.tank_mental_health.level / self.tank_mental_health.capacity,
            'physical_health': self.tank_physical_health.level / self.tank_physical_health.capacity,
            'leisure': self.tank_leisure.level / self.tank_leisure.capacity,
            'social_inclusion': self.tank_social_inclusion.level / self.tank_social_inclusion.capacity,
            'self_determination': self.tank_self_determination.level / self.tank_self_determination.capacity,
            'food': self.tank_food.level / self.tank_food.capacity
        }

    def show_tanks(self):
        print(f"Mental-Health:  {self.tank_mental_health.level}; "
              f"Physical-Health: {self.tank_physical_health.level}; "
              f"Leisure-Tank: {self.tank_leisure.level}; "
              f"social-inclusion: {self.tank_social_inclusion.level}; "
              f"self-determination: {self.tank_self_determination.level}; ",
              f"food: {self.tank_food.level};"
              )

    def best_location_for_tanks(self, tanks):
        # tanks: Liste von Strings, z.B. ['mental_health', 'food']
        location_map = {
            'mental_health': ['home'],
            'physical_health': ['park'],
            'leisure': ['home'],
            'social_inclusion': ['park'],
            'self_determination': ['home'],
            'food': ['supermarket']
        }
        locations = []
        for tank in tanks:
            locations.extend(location_map.get(tank, []))
        return list(set(locations))

    def quality_of_life(self):
        mental_health = self.tank_mental_health.level
        physical_health = self.tank_physical_health.level
        self_determination = self.tank_self_determination.level
        self_leisure = self.tank_leisure.level
        social_inclusion = self.tank_social_inclusion.level
        self.life_quality = mental_health + physical_health + self_determination + self_leisure + social_inclusion



