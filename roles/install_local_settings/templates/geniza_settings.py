{% extends "settings.py" %}
"""
Django local settings for geniza
"""

{% block extra_config %}
# Use x-forwarded-proto header to tell if request from nginx was https or not
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# urls to google sheets data published as csv for import
DATA_IMPORT_URLS = {
    'libraries': '{{ libraries_csv_url }}',
    'languages': '{{ languages_csv_url }}',
    'metadata': '{{ metadata_csv_url }}'
}

# path to preliminary JSON transcription data
TRANSCRIPTIONS_JSON_FILE = "/srv/www/geniza/data/transcriptions.json"

{% endblock %}

{% block solr_config %}
from geniza.settings.components.base import SOLR_CONNECTIONS

SOLR_CONNECTIONS['default']['URL'] = "{{ solr_url }}"
SOLR_CONNECTIONS['default']['COLLECTION'] = "{{ solr_collection }}"
SOLR_CONNECTIONS['default']['CONFIGSET'] = "{{ solr_configset }}"

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
        'geniza': {
            'handlers': ['debug_log'],
            'level': 'WARN',
            'propagate': True,
        },
        'parasolr': {
            'handlers': ['debug_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
{% endblock %}
