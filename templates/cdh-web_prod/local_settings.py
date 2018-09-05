# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

DEBUG = False

# compress offline
COMPRESS_OFFLINE = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "{{ secret_key }}"
NEVERCACHE_KEY = "{{ nevercache_key }}"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.mysql",
        # DB name or path to database file if using sqlite3.
        "NAME": "{{ db_name }}",
        # Not used with sqlite3.
        "USER": "{{ db_username }}",
        # Not used with sqlite3.
        "PASSWORD": "{{ db_password }}",   # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "{{ db_host }}",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}



###################
# DEPLOY SETTINGS #
###################

# Domains for public site
ALLOWED_HOSTS = ["cdh-web.princeton.edu", "cdh.princeton.edu",
                 "digitalhumanities.princeton.edu"]

#
ADMINS = [('CDH Dev Team', 'cdhdevteam@princeton.edu')]
SERVER_EMAIL = 'cdhdevteam@princeton.edu'

# Email configuration for sending messages

EMAIL_HOST = 'smtp.princeton.edu'
EMAIL_HOST_USER = 'cdhdevteam'
EMAIL_HOST_PASSWORD = '{{ email_host_password }}'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = '[CDH Web 2.0+ Production] '

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
}


{% include 'templates/common/cas_configuration.py' %}


# Media root settings for production
MEDIA_ROOT = '/srv/www/media/'
MEDIA_URL = '/media/'

# Allow SVG
FILEBROWSER_ESCAPED_EXTENSIONS = []
