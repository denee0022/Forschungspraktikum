from constants import Activity


class DailySchedule:
    def __init__(self, steps_per_day=8):
        self.steps_per_day = steps_per_day
        self.schedule = {
            0: Activity.SLEEPING,
            1: Activity.WORKING,
            2: Activity.WORKING,
            3: Activity.WORKING,
            6: Activity.LEISURE,
            7: Activity.LEISURE,
            8: Activity.SLEEPING
        }

    def get_activity_for_step(self, step):
        day_step = step % self.steps_per_day
        return self.schedule.get(day_step, Activity.SLEEPING)

    def get_next_activity_change(self, current_step):
        current_activity = self.get_activity_for_step(current_step)
        for i in range(1, self.steps_per_day):
            next_step = (current_step + i) % self.steps_per_day
            if self.get_activity_for_step(next_step) != current_activity:
                return next_step
        return None
