from enum import Enum


class Activity(Enum):
    SLEEPING = 0
    WAKING_UP = 1
    WORKING = 2
    LEISURE = 3

class PreferenceType(Enum):
    MENTAL_HEALTH = "mental_health"
    PHYSICAL_HEALTH = "physical_health"
    LEISURE = "leisure"
    EFFICIENCY = "efficiency"
    GREEN_ENVIRONMENT = "green_environment"
    SOCIAL_INCLUSION = "social_inclusion"
    SELF_DETERMINATION = "self_determination"
    FOOD = "food"
