{% extends 'templates/common/base.py' %}

{% block extra_config %}
{# Add static root as needed now because missing from settings.py as of 0.7 #}
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Separate Geonames for usage reasons
GEONAMES_USERNAME = '{{ geonames_username }}'
# Mapbox token shared with Winthrop
MAPBOX_ACCESS_TOKEN = '{{ mapbox_token }}'
# Media settings for running under apache in production and QA
MEDIA_ROOT = '{{ media_root }}'
MEDIA_URL = '/media/'

# OCLC API key
OCLC_WSKEY = '{{ oclc_wskey }}'

# Email address for a technical contact.
# Will be used in From header for OCLC API requests
TECHNICAL_CONTACT = '{{ technical_contact }}'

# font settings so that licensed fonts are copied over
{% if qa is defined and qa %}
STATICFILES_DIRS += [
    '/srv/www/qa/mep-django/fonts'
]
{% else %}
STATICFILES_DIRS += [
    '/srv/www/prod/fonts'
]
{% endif %}

SOLR_CONNECTIONS = {
    'default': {
        'URL': '{{ solr_url }}',
        'COLLECTION': '{{ solr_collection }}',
        'CONFIGSET': '{{ solr_configset }}'
    }
}

{% endblock %}

{% block logging %}
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
        {# This configuration lets logrotate and its proper permissions #}
        {# handle this problem #}
        'debug_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '{{ logging_path }}',
            'formatter': 'basic',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'debug_log'],
            'level': 'ERROR',
            'propagate': True,
        },
        'mep': {
            'handlers': ['debug_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
{% endblock %}

# turn on google analytics
GTAGS_ANALYTICS_ID = 'UA-87887700-6'
{% if qa is defined and qa %}
GTAGS_ANALYTICS_ENV = 'qa'
{% else %}
GTAGS_ANALYTICS_ENV = 'prod'
{% endif %}

# configure content security policy reporting
{% if qa is defined and qa %}
CSP_REPORT_ONLY = True
CSP_REPORT_URI = '{{ csp_reportonly_uri }}'
{% else %}
CSP_REPORT_ONLY = False
CSP_REPORT_URI = '{{ csp_enforce_uri }}'
{% endif %}
