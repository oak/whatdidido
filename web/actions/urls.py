__author__ = 'adcarvalho'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url('^$', 'web.actions.views.list', name='action-list'),
    url('^create/$', 'web.actions.views.create', name='action-create'),
    url('^edit/(?P<id>\d*)$', 'web.actions.views.edit', name='action-edit'),
)