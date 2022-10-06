{% extends "local_settings.py" %}
"""
Django local settings for geniza
"""

{% block extra_config %}
# Use x-forwarded-proto header to tell if request from nginx was https or not
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

TEI_TRANSCRIPTIONS_LOCAL_PATH = "/srv/www/geniza/data/tei_xml/"

# TinyMCE API key
TINY_API_KEY = '{{ tiny_api_key }}'

{% if qa is not defined %}
GTAGS_ANALYTICS_ID = "G-3HMY094CY2"
{% endif %}

# base url for simple annotation server
ANNOTATION_SERVER_URL = "{{ annotation_server_url }}"
# base url for manifest uris used with annotation server
ANNOTATION_MANIFEST_BASE_URL = "https://geniza.princeton.edu"

# URL for git repository of transcription annotation backups
ANNOTATION_BACKUP_GITREPO = "{{ annotation_backup_gitrepo }}"
# local path where git repo should be cloned
ANNOTATION_BACKUP_PATH = "{{ annotation_backup_path }}"


FEATURE_FLAGS = [
    {% if show_warning_banner %}
    "SHOW_WARNING_BANNER", # show warning banner
    {% endif %}
]
# Configure warning banner when set
{% if warning_banner_heading %}
WARNING_BANNER_HEADING = "{{ warning_banner_heading }}"
{% endif %}
{% if warning_banner_message %}
WARNING_BANNER_MESSAGE = "{{ warning_banner_message }}"
{% endif %}


# Languages to make visible on the public site/front-end in addition to the admin site.
# If undefined, all LANGUAGES will be enabled on both the public and admin site.
# Must be a subset of the language codes in LANGUAGES from base settings, or undefined.
# For production only, limit to languages ready to be made public
PUBLIC_SITE_LANGUAGES = [
   "en",
{% if qa is defined %}
   "he",
{% endif %}
#    "he",
#    "ar",
]
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
