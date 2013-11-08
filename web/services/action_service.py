from web.models import Action

__author__ = 'adcarvalho'


class ActionService():
    def get_latest_actions(self, user, count):
        return Action.objects.filter(user=user).order_by('-date')[:count]

