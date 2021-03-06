from django.conf.urls import patterns, include, url
import autocomplete_light

autocomplete_light.autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web.views.home', name='home'),
    url(r'^login/', 'web.views.login', name='login'),
    url(r'^logout/$', 'web.views.logout', name='logout'),

    url(r'^actions/', include('web.actions.urls')),
    url(r'^things/', include('web.things.urls')),

    url(r'^reset-schedule/$', 'web.views.reset_schedule', name='reset-schedule'),

    url(r'autocomplete/', include('autocomplete_light.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
