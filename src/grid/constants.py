from enum import Enum


class Activity(Enum):
    SLEEPING = 0
    WAKING_UP = 1
    WORKING = 2
    LEISURE = 3


# Schauen, ob man dies benutzt für Sauberkeit
class LocationType(Enum):
    HOME = 0
    WORKPLACE = 1
    PARK = 2
    SUPERMARKET = 3
