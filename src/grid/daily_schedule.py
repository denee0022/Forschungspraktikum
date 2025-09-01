from constants import Activity


class DailySchedule:
    def __init__(self, steps_per_day=24):
        #Nochmal nachschauen wie man es effektiv machen sonst einfach manuell hinzufügen
        self.steps_per_day = steps_per_day
        self.schedule = {
            {0, 1, 2, 3, 4, 5, 6, 7, 22, 23}: Activity.SLEEPING,
            {8, 9, 10, 11, 12, 13, 14, 15, 16}: Activity.WORKING,
            {17, 18, 19, 20, 21}: Activity.LEISURE
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
