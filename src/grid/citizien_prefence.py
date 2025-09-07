import numpy as np
from constants import PreferenceType


class CitizienPreferences:
    def __init__(self, preference_tank_weights=None, preference_route_weights=None):
        # Intialize tank preferences to decide which need to fill up
        if preference_tank_weights is None:
            self.tank_weights = {
                PreferenceType.MENTAL_HEALTH: np.random.uniform(0.1, 0.9),
                PreferenceType.PHYSICAL_HEALTH: np.random.uniform(0.1, 0.9),
                PreferenceType.LEISURE: np.random.uniform(0.1, 0.9),
                PreferenceType.SOCIAL_INCLUSION: np.random.uniform(0.1, 0.9),
                PreferenceType.SELF_DETERMINATION: np.random.uniform(0.1, 0.9),
                PreferenceType.FOOD: np.random.uniform(0.1, 0.9)
            }
        else:
            self.tank_weights = preference_tank_weights

        # Initialize route preferences to decide which route to take
        if preference_route_weights is None:  # Separate Behandlung für route_weights
            self.route_weights = {
                PreferenceType.EFFICIENCY: np.random.uniform(0.1, 0.9),
                PreferenceType.GREEN_ENVIRONMENT: np.random.uniform(0.1, 0.9)
            }
        else:
            self.route_weights = preference_route_weights

        # normalize the weights
        total_tank_weight = sum(self.tank_weights.values())
        for pref_type in self.tank_weights:
            self.tank_weights[pref_type] /= total_tank_weight

        total_route_weight = sum(self.route_weights.values())
        for pref_type in self.route_weights:
            self.route_weights[pref_type] /= total_route_weight

    def get_tank_weight(self, preference_type: PreferenceType) -> float:
        return self.tank_weights.get(preference_type, 0.0)

    def get_route_weight(self, preference_type: PreferenceType) -> float:
        return self.route_weights.get(preference_type, 0.0)

    def get_preference_tank_vector(self) -> np.ndarray:
        return np.array([
            self.tank_weights[PreferenceType.MENTAL_HEALTH],
            self.tank_weights[PreferenceType.PHYSICAL_HEALTH],
            self.tank_weights[PreferenceType.LEISURE],
            self.tank_weights[PreferenceType.SOCIAL_INCLUSION],
            self.tank_weights[PreferenceType.SELF_DETERMINATION],
            self.tank_weights[PreferenceType.FOOD]

        ])

    def get_preference_route_vector(self) -> np.ndarray:
        return np.array([
            self.route_weights[PreferenceType.EFFICIENCY],
            self.route_weights[PreferenceType.GREEN_ENVIRONMENT]
        ])

    def show_preferences(self):
        print(f"Route-Präferenz-Vektoren: {self.get_preference_route_vector()}")
        print(f"Tank-Präferenz-Vektoren: {self.get_preference_tank_vector()}")

    def get_highest_tank_preference_type(self):
        return max(self.tank_weights, key=self.tank_weights.get)

    def get_highest_route_preference_type(self):
        return max(self.route_weights, key=self.route_weights.get)
