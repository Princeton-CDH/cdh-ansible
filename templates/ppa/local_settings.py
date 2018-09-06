{% extends 'templates/common/base.py' %}

# PPA local settings
# with configurations that should *not* be checked into version control

{% block solr_config %}
SOLR_CONNECTIONS = {
    'default': {
        'COLLECTION': '{{ solr_collection }}',
        'URL': '{{ solr_url }}',
        'ADMIN_URL': '{{ solr_admin_url }}'
    },
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
        'debug_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
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
            'level': 'DEBUG',
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

# Turn on Google Analytics
INCLUDE_ANALYTICS = True

# Add offline compression for QA/PROD servers
COMPRESS_OFFLINE = True

{% if qa is not defined %}
# turn on google analytics
INCLUDE_ANALYTICS = True
{% endif %}
{% endblock %}


