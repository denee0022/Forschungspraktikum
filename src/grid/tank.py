class Tank:
    def __init__(self, capacity, level, threshold):
        self.capacity = capacity
        self.level = level
        self.threshold = threshold

    def update(self, amount):
        # Nettofluss
        self.level += amount
        # Begrenzung durch Tankvolumen
        if self.level > self.capacity:
            overflow = self.level - self.capacity
            self.level = self.capacity
            return overflow
        elif self.level < 0:
            deficit = -self.level
            self.level = 0
            return -deficit
        return 0.0