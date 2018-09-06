{% extends 'templates/common/base.py' %}

{% block basic_settings %}
{{ super() }}
NEVERCACHE_KEY = "{{ nevercache_key }}"
{% endblock %}

{% block logging %}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
}
{% endblock %}

{% block extra_config %}
# set compress offline for django-compressor
COMPRESS_OFFLINE = True

# Media root settings for production
MEDIA_ROOT = '/srv/www/media/'
MEDIA_URL = '/media/'

# Allow SVG
FILEBROWSER_ESCAPED_EXTENSIONS = []
{% endblock %}
