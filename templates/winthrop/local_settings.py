{% extends 'templates/common/base.py' %}

{% block solr_config %}
{# temmporarily restrict to QA #}
{% if qa is defined %}
SOLR_CONNECTIONS = {
    'default': {
        'COLLECTION': '{{ solr_collection }}',
        'URL': '{{ solr_url }}',
        'ADMIN_URL': '{{ solr_admin_url }}'
    },
}
{% endif %}
{% endblock %}

{% block logging %}
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
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{{ logging_path }}',
            'formatter': 'basic',
            'maxBytes': 1024,
            'backupCount': 3
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
    }
}
{% endblock %}

{% block extra_config %}
# username for accessing GeoNames API
GEONAMES_USERNAME = '{{ geonames_username }}'
# mapbox access token
MAPBOX_ACCESS_TOKEN = '{{ mapbox_token }}'
# Add offline compression for QA/PROD servers
COMPRESS_OFFLINE = True
# temporarily disable compression for QA and testing
COMPRESS_JS_FILTERS = []
{% if qa is not defined %}
# turn on google analytics
INCLUDE_ANALYTICS = True
{% endif %}
{% endblock %}
