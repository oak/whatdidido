from django.db.models import Max
from web.models import Action, Schedule, Thing
from datetime import datetime, timedelta
import numpy

__author__ = 'adcarvalho'

LIMIT_PERCENTAGE = 0.5

class ActionService():
    def get_latest_actions(self, user, count):
        return Action.objects.filter(user=user).order_by('-date')[:count]

    def get_scheduled_actions(self, user, count):
        return Schedule.objects.filter(user=user).order_by('date')[:count]

    def set_next_schedule(self, user, thing):
        actions_for_thing = Action.objects.filter(user=user, thing=thing).order_by('date')

        time_deltas = []
        for index in range(len(actions_for_thing) - 1, 0, -1):
            time_delta = actions_for_thing[index].date - actions_for_thing[index - 1].date
            time_deltas.append((actions_for_thing[index].date, actions_for_thing[index - 1].date, time_delta.days * 24 + time_delta.seconds / 3600))

        if len(time_deltas) == 0:
            return

        time_deltas_deltas = [row[2] for row in time_deltas]

        mean = numpy.mean(time_deltas_deltas)
        std = numpy.std(time_deltas_deltas)

        inside_interval = 0
        for time_delta in time_deltas_deltas:
            inside_interval += 1 if time_delta <= mean + std and time_delta >= mean - std else 0

        if mean * LIMIT_PERCENTAGE > std:
            new_sched = Schedule()
            new_sched.date = actions_for_thing[len(actions_for_thing) - 1].date + timedelta(hours=abs(mean))
            new_sched.user = user
            new_sched.thing = thing
            new_sched.save()

    def reset_next_schedule(self, user, thing):
        pending_schedules = Schedule.objects.filter(user=user, thing=thing, status=Schedule.Status.PENDING).delete()

        self.set_next_schedule(user, Thing.objects.get(id=thing.id))

    def reset_next_schedules(self, user):
        pending_schedules = Schedule.objects.filter(user=user, status=Schedule.Status.PENDING).delete()

        things = Action.objects.filter(user=user).values('thing').annotate(max_id=Max('date'))

        for thing in things:
            self.set_next_schedule(user, Thing.objects.get(id=thing['thing']))
