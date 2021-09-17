"""
ASGI config for back_end project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('SETTINGS_PATH', cast=str))

application = get_asgi_application()
