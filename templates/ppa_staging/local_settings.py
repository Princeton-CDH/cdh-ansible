# Sample local settings
# Copy to derrida/local_settings.py and configure
# includes sensitive configurations, should *not* be
# checked into version control

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# SECURITY WARNING: keep the secret key used in production secret!
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = "{{ secret_key }}"


# Turn this on in test/QA site to show test banner
#SHOW_TEST_WARNING = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
    'NAME': '{{ db_name }}',
    'USER': '{{ db_username }}',
    'PASSWORD': '{{ db_password}}',
    'HOST': '{{ db_host }}',
    'PORT': '3306',
    'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
       }
    }
}


SOLR_CONNECTIONS = {
    'default': {
        'COLLECTION': '{{ solr_collection }}',
        'URL': '{{ solr_url }}',
        'ADMIN_URL': '{{ solr_admin_url }}'
    },
}

# local path to hathi pairtree data provided via rsync
HATHI_DATA = '/path/to/hathi_pairtree_root'

# Enable django-compressor compression
COMPRESS = True

COMPRESS_ENABLED = True

COMPRESS_OFFLINE = True

# include CAS configuration from file
{% include 'templates/common/cas_configuration.py' %}


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL.strip("/"))

# Admin email configuration for error messages
# ADMINS = [('name', 'email')]
# SERVER_EMAIL = '

# Email configuration for sending messages
EMAIL_SUBJECT_PREFIX = '[PPA] '

# Solution following https://stackoverflow.com/a/9541647
# Sends a logging email even when DEBUG is on
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

