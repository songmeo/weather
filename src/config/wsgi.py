"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    from config import secret
    os.environ.setdefault('SECRET_KEY', secret.SECRET_KEY)
    os.environ.setdefault('API_KEY', secret.API_KEY)
except ImportError: # config.secret is missing
    pass

application = get_wsgi_application()
