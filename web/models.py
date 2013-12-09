from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Profile(models.Model):
    phone = models.CharField(max_length=30, null=True, blank=True)
    cell = models.CharField(max_length=30, null=True, blank=True)
    picture = models.FileField(upload_to='profile')
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.get_full_name()


class Thing(models.Model):
    name = models.CharField(null=False, blank=False, max_length=1024)
    usage_count = models.BigIntegerField(null=False, default=0)

    def __unicode__(self):
        return self.name


class Action(models.Model):
    thing = models.ForeignKey(Thing, null=False, related_name='actions')
    date = models.DateTimeField(null=False)
    picture = models.FileField(upload_to='action', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='actions')

    def __unicode__(self):
        return unicode(self.thing) + u' @ ' + unicode(self.date)


class Schedule(models.Model):
    class Status(object):
        PENDING = 0
        IGNORED = 1
        DONE = 2
        MUTED = 3
    user = models.ForeignKey(User, null=False, related_name='schedules')
    thing = models.ForeignKey(Thing, null=False, related_name='schedules')
    date = models.DateTimeField(null=False)
    status = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    created = models.DateTimeField(null=False, auto_now_add=True)


def action_pre_save(sender, instance, **kwargs):
    if not instance.date:
        instance.date = datetime.now()
    instance.thing.usage_count += 1
    instance.thing.save()


def action_pre_delete(sender, instance, **kwargs):
    instance.thing.usage_count -= 1
    instance.thing.save()

def action_reset_schedule(sender, instance, **kwargs):
    from web.services.action_service import ActionService
    action_service = ActionService()
    action_service.reset_next_schedule(instance.user, instance.thing)

models.signals.pre_save.connect(action_pre_save, sender=Action, dispatch_uid='action_pre_save_thing_count')
models.signals.pre_delete.connect(action_pre_delete, sender=Action, dispatch_uid='action_pre_delete_thing_count')
models.signals.post_save.connect(action_reset_schedule, sender=Action, dispatch_uid='action_reset_schedule')
models.signals.post_delete.connect(action_reset_schedule, sender=Action, dispatch_uid='action_reset_schedule')

