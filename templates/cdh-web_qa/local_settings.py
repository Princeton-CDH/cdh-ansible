# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

DEBUG = False

# Make these unique, and don't share it with anybody.
SECRET_KEY = "{{ secret_key }}"
NEVERCACHE_KEY = "{{ nevercache_key}}"

# override default media config so it is shared across deploys
MEDIA_ROOT = '/srv/www/qa/cdh-web/media'
MEDIA_URL = '/media/'

SHOW_TEST_WARNING = True
å
DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.mysql",
        # "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        # "NAME": "dev.db",
        "NAME": "{{ db_name }}",
        # Not used with sqlite3.
        "USER": "{{ db_username }}",
        # Not used with sqlite3.
        "PASSWORD": "{{ db_username }}",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}


{% include 'templates/common/cas_configuration.py' %}



###################
# DEPLOY SETTINGS #
###################

# Domains for public site
ALLOWED_HOSTS = ["test-web.cdh.princeton.edu"]

# Admin email settings for error messages
ADMINS = [('CDH Dev Team', 'cdhdevteam@princeton.edu')]
SERVER_EMAIL = 'cdhdevteam@princeton.edu'

# Email configuration for sending messages
EMAIL_SUBJECT_PREFIX = '[CDH Web - QA] '


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
