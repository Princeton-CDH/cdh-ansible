{% extends 'templates/common/base.py' %}

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
# Add Google Analytics
INCLUDE_ANALYTICS = True
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
