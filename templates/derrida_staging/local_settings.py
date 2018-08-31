# local settings for sensitive configurations that should not be
# checked into version control

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Insecure setting for staging vagrant isntance only!
ALLOWED_HOSTS = ['*']

# SECURITY WARNING: keep the secret key used in production secret!
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = '{{ secret_key }}'

# Separate Geonames for usage reasons
GEONAMES_USERNAME = '{{ geonames_username }}'
# Mapbox token shared with Winthrop
MAPBOX_ACCESS_TOKEN = '{{ mapbox_token }}'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'derrida.common.solr_backend.RangeSolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/derrida',
        'ADMIN_URL': 'http://127.0.0.1:8983/solr/admin/cores'
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'derrida.books.signals.RelationSafeRTSP'

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ db_name }}',
        'USER': '{{ db_username }}',
        'PASSWORD': '{{ db_password}}',
        'HOST': '{{ db_host }}',
        'PORT': '',
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    },
}



DJIFFY_AUTH_TOKENS = {
    'plum.princeton.edu': '{{ plum_token }}',
    'figgy.princeton.edu': '{{ figgy_token }}',
}

# Admin email settings for error messages
ADMINS = [('CDH Dev Team', 'cdhdevteam@princeton.edu')]
SERVER_EMAIL = 'cdhdevteam@princeton.edu'

# Email configuration for sending messages

EMAIL_HOST = 'smtp.princeton.edu'
EMAIL_HOST_USER = 'cdhdevteam'
EMAIL_HOST_PASSWORD = '{{ email_host_password }}'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = '[Derridas Margins Prod] '

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
            'filename': '/srv/www/prod/derrida.log',
            'formatter': 'basic',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'debug_log'],
            'level': 'ERROR',
            'propagate': True,
        },
        'derrida': {
            'handlers': ['debug_log'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}


# set compress offline to true
COMPRESS_OFFLINE = True

# turn on google analytics
INCLUDE_ANALYTICS = True
