{% extends 'settings.py' %}

# PPA local settings
# with configurations that should *not* be checked into version control

{% block solr_config %}
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
            'level': 'INFO',
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
        'ppa': {
            'handlers': ['debug_log'],
            'level': 'INFO',
            'propagate': True,
        },
        'SolrClient':  {
            'handlers': ['debug_log'],
            'level': 'WARN'
        },

    }
}
{% endblock %}

{% block extra_config %}
# Set local path to HathiTrust pairtree data provided via rsync
HATHI_DATA = '{{ hathitrust_pairtree_path }}'

# credentials for HathiTrust Data API
HATHITRUST_OAUTH_KEY = '{{ hathitrust_oauth_key }}'
HATHITRUST_OAUTH_SECRET = '{{ hathitrust_oauth_secret }}'

# Email address for a technical contact.
# Will be used in From header for HathiTrust API requests
TECHNICAL_CONTACT = '{{ technical_contact }}'


# Turn on Google Analytics
INCLUDE_ANALYTICS = True

# Media settings for running under apache in production and QA
MEDIA_ROOT = '{{ media_root }}'
MEDIA_URL = '/media/'


{% if qa is not defined %}
# turn on google analytics
GTAGS_ANALYTICS_ID = 'UA-87887700-5'
{% endif %}
{% endblock %}
