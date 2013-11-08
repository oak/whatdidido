__author__ = 'adcarvalho'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url('^$', 'web.things.views.list', name='thing-list'),
    url('^create/$', 'web.things.views.create', name='thing-create'),
    url('^edit/(?P<id>\d*)$', 'web.things.views.edit', name='thing-edit'),
)