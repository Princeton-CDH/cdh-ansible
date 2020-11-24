{% extends 'settings.py' %}

{% block solr_config %}
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'derrida.common.solr_backend.RangeSolrEngine',
        'URL': '{{ solr_url }}{{ solr_collection }}',
        'ADMIN_URL': '{{ solr_admin_url }}'
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'derrida.books.signals.RelationSafeRTSP'
{% endblock %}

{% block extra_config %}
# Separate Geonames for usage reasons
GEONAMES_USERNAME = '{{ geonames_username }}'
# Mapbox token shared with Winthrop
MAPBOX_ACCESS_TOKEN = '{{ mapbox_token }}'

# Zotero API key and Group library for exporting book data
ZOTERO_API_KEY = '{{ zotero_api_key }}'
ZOTERO_LIBRARY_ID = '{{ zotero_library_id }}'

DJIFFY_AUTH_TOKENS = {
    'plum.princeton.edu': '{{ plum_token }}',
    'figgy.princeton.edu': '{{ figgy_token }}',
}

# Media settings for running under apache in production and QA
MEDIA_ROOT = '{{ media_root }}'
MEDIA_URL = '/media/'

# set compress offline for Django Compressor
COMPRESS_OFFLINE = True
{% if qa is not defined %}
# turn on google analytics
INCLUDE_ANALYTICS = True
{% endif %}

{% endblock %}

{% block logging %}
# FIXME: permissions error on log file

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
        'file_log': {
            'level': 'WARN',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '{{ logging_path }}',
            'formatter': 'basic',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file_log'],
            'level': 'ERROR',
            'propagate': True,
        },
        'derrida': {
            'handlers': ['file_log'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
{% endblock %}

