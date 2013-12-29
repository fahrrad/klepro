"""
WSGI config for klepro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, dj_static
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "klepro.settings")

from django.core.wsgi import get_wsgi_application
application = dj_static.Cling(get_wsgi_application())
