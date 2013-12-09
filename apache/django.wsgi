import os
import sys

path = '/var/www'
if path not in sys.path:
    sys.path.insert(0, '/var/www')
    sys.path.insert(1, '/var/www/whatdidido')

os.environ['DJANGO_SETTINGS_MODULE'] = 'whatdidido.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
