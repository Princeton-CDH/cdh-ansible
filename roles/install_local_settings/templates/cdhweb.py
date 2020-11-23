{% extends 'base.py' %}

{% block basic_settings %}
{{ super() }}
NEVERCACHE_KEY = "{{ nevercache_key }}"
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
        'cdhweb': {
            'handlers': ['debug_log'],
            'level': 'WARN',
            'propagate': True,
        },
    }
}
{% endblock %}

{% block extra_config %}
# set compress offline for django-compressor
COMPRESS_OFFLINE = True

# Media root settings for production
MEDIA_ROOT = '{{ media_root }}'
MEDIA_URL = '/media/'

# Allow SVG
FILEBROWSER_ESCAPED_EXTENSIONS = []

# managers for broken email 404s
MANAGERS = [('CDH Dev Team', 'cdhdevteam@princeton.edu'),]
# ignore php, asp, aspx, jsp, jspa, with or without trailing slash
import re
IGNORABLE_404_URLS = [re.compile('\.(php|aspx?|jspa?)(\/$|$)')]
{% endblock %}
