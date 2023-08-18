class ScheduleMap:
    def __init__(self, schedule):
        self.schedule: dict[str, list] = schedule

    def room_mode_to_cohort(self):
        cohort_schedule = dict()
        for room_name, schedules in self.schedule.items():
            for schedule in schedules:
                subject = schedule['subject']

