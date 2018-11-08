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
MEDIA_ROOT = '{{ media_root }}'
MEDIA_URL = '/media/'

# Allow SVG
FILEBROWSER_ESCAPED_EXTENSIONS = []

# managers for broken email 404s
MANAGERS = [('CDH Dev Team', 'cdhdevteam@princeton.edu'),]
# ignore .php and as(p|x), also handle trailing slash being appended
IGNORABLE_404_URLS = ['(\.php|\.asp|\.aspx)(\/$|$)']
{% endblock %}
