from constants import Activity


class DailySchedule:
    def __init__(self, steps_per_day=24):
        #Nochmal nachschauen wie man es effektiv machen sonst einfach manuell hinzufügen
        self.steps_per_day = steps_per_day
        self.schedule = {}

        for hour in [0, 1, 2, 3, 4, 5, 6, 7, 22, 23]:
            self.schedule[hour] = Activity.SLEEPING

        for hour in range(8, 17):
            self.schedule[hour] = Activity.WORKING

        for hour in range(17, 22):
            self.schedule[hour] = Activity.LEISURE
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
