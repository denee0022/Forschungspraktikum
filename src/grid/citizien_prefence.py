import numpy as np
from constants import PreferenceType


class CitizienPreferences:
    def __init__(self, preference_weights=None):
        if preference_weights is None:
            self.weights = {
                PreferenceType.MENTAL_HEALTH: np.random.uniform(0.1, 0.9),
                PreferenceType.PHYSICAL_HEALTH: np.random.uniform(0.1, 0.9),
                PreferenceType.LEISURE: np.random.uniform(0.1, 0.9),
                PreferenceType.EFFICIENCY: np.random.uniform(0.1, 0.9),
                PreferenceType.GREEN_ENVIRONMENT: np.random.uniform(0.1, 0.9),
                PreferenceType.SOCIAL_INCLUSION: np.random.uniform(0.1, 0.9),
                PreferenceType.SELF_DETERMINATION: np.random.uniform(0.1, 0.9),
                PreferenceType.FOOD: np.random.uniform(0.1, 0.5)
            }
        else:
            self.weights = preference_weights

        total_weight = sum(self.weights.values())
        for pref_type in self.weights:
            self.weights[pref_type] /= total_weight

    def get_weight(self, preference_type: PreferenceType) -> float:
        return self.weights.get(preference_type, 0.0)

    def get_preference_vector(self) -> np.ndarray:
        return np.array([
            self.weights[PreferenceType.MENTAL_HEALTH],
            self.weights[PreferenceType.PHYSICAL_HEALTH],
            self.weights[PreferenceType.LEISURE],
            self.weights[PreferenceType.EFFICIENCY],
            self.weights[PreferenceType.GREEN_ENVIRONMENT]
        ])
