'''
Created on 2011/5/5

@author: korprulu
'''
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_URLCONF = 'urls'  # Replace 'project.urls' with just 'urls'

LANGUAGE_CODE = 'zh-tw'

TIME_ZONE = 'Asia/Taipei'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

INSTALLED_APPS = (
#    'django.contrib.auth',
    'django.contrib.contenttypes',
#    'django.contrib.sessions',
    'django.contrib.sites',
)

INSTALLED_APPS += ('file.youtube',)

ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".  Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ROOT_PATH + '/templates',
)