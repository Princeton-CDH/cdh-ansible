# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

DEBUG = False

SHOW_TEST_WARNING = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = '^^ secret_key ^^'

# username for accessing GeoNames API
GEONAMES_USERNAME = '{{ geonames_username }}'

# mapbox access token
MAPBOX_ACCESS_TOKEN = '^^ mapbox_token ^^'

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.mysql",
        # "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        # "NAME": "dev.db",
        "NAME": "^^ db_name ^^",
        # Not used with sqlite3.
        "USER": "^^ db_username ^^",
        # Not used with sqlite3.
        "PASSWORD": "^^ db_password ^^",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
	"OPTIONS": {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

SOLR_CONNECTIONS = {
    'default': {
        'COLLECTION': 'winthrop',
        'URL': 'http://127.0.0.1:8983/solr/',
        'ADMIN_URL': 'http://127.0.0.1:8983/solr/admin/cores'
    },
   'test': {
        'COLLECTION': 'winthrop-test',
        'URL': 'http://127.0.0.1:8983/solr/',
        'ADMIN_URL': 'http://127.0.0.1:8983/solr/admin/cores'
    }
}

CAS_SERVER_URL = 'https://fed.princeton.edu/cas/'

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
ALLOWED_HOSTS = ["test-winthrop.cdh.princeton.edu"]

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

# Admin email settings for error messages
ADMINS = [('CDH Dev Team', 'cdhdevteam@princeton.edu')]
SERVER_EMAIL = 'cdhdevteam@princeton.edu'

# Email configuration for sending messages
EMAIL_SUBJECT_PREFIX = '[Winthrop - QA] '


# Solution following https://stackoverflow.com/a/9541647
# Sends a logging email even when DEBUG is on
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'basic': {
            'format': '[%(asctime)s] %(levelname)s:%(name)s::%(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },
        'debug_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/srv/www/qa/winthrop-django/winthrop.log',
            'formatter': 'basic',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'debug_log'],
            'level': 'ERROR',
            'propagate': True,
        },
        'winthrop': {
            'handlers': ['debug_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'SolrClient':  {
            'handlers': ['debug_log'],
            'level': 'WARN'
        },

    }
}

# Add offline compression for QA/PROD servers
COMPRESS_OFFLINE = True
# temporarily disable compression for QA and testing
COMPRESS_JS_FILTERS = []
