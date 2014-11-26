"""
WSGI config for Marine Planner CROP
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mp.settings")

activate_this = '/home/crop/env/marine-planner/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
