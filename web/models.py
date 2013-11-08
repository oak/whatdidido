from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    phone = models.CharField(max_length=30, null=True, blank=True)
    cell = models.CharField(max_length=30, null=True, blank=True)
    picture = models.FileField(upload_to='profile')
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.get_full_name()


class Thing(models.Model):
    name = models.TextField(null=False, blank=False)
    usage_count = models.BigIntegerField(null=False, default=0)

    def __unicode__(self):
        return self.name


class Action(models.Model):
    thing = models.ForeignKey(Thing, null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)
    picture = models.FileField(upload_to='action')
    description = models.TextField()
    user = models.ForeignKey(User, related_name='actions')

    def __unicode__(self):
        return unicode(self.thing) + u' @ ' + unicode(self.date)