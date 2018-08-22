# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.
# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

# Add Google Analytics
INCLUDE_ANALYTICS = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "{{ secret_key }}"

# username for accessing GeoNames API
GEONAMES_USERNAME = '{{ geonames_username }}'
# mapbox access token
MAPBOX_ACCESS_TOKEN = '{{ mapbox_token }}'

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

CAS_SERVER_URL = 'https://fed.princeton.edu/cas/'

CAS_VERSION = '3'

PUCAS_LDAP.update({
    'SERVERS': [
        'ldap2.princeton.edu',
        'ldap3.princeton.edu',
        'ldap4.princeton.edu',
        'ldap5.princeton.edu'
    ],
    'SEARCH_BASE': 'o=Princeton University,c=US',
    'SEARCH_FILTER': "(uid=%(user)s)",
    # other ldap attributes we might want:
    # ou = organizational unit
})


###################
# DEPLOY SETTINGS #
###################

# Domains for public site
ALLOWED_HOSTS = ["winthrop.princeton.edu"]
DEBUG = False

# Settings similar to mezzanine for static file deploy
# Full filesystem path to the project.
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))


ADMINS = [('CDH Dev Team', 'cdhdevteam@princeton.edu')]
SERVER_EMAIL = 'cdhdevteam@princeton.edu'

# Email configuration for sending messages

EMAIL_HOST = 'smtp.princeton.edu'
EMAIL_HOST_USER = 'cdhdevteam'
EMAIL_HOST_PASSWORD = '{{ email_host_password }}'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = '[Winthrop Prod] '

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
