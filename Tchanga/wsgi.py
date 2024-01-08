"""
WSGI config for Tchanga project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.servers.basehttp import get_wsgi_application
#from django.core.wsgi import get_wsgi_application
#project_path = '/home/alassane/Desktop/Dev-Projects/PythonProjects/Django/Tchanga/'
#sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tchanga.settings')

application =get_wsgi_application()

#app =application