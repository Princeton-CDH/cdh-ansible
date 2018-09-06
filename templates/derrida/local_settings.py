{% extends 'templates/common/base.py' %}

{% block solr_config %}
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'derrida.common.solr_backend.RangeSolrEngine',
        'URL': '{{ solr_url }}',
        'ADMIN_URL': '{{ solr_admin_url }}'
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'derrida.books.signals.RelationSafeRTSP'
{% endblock %}

{% block logging %}
{% endblock %}

{% block extra_config %}
# Separate Geonames for usage reasons
GEONAMES_USERNAME = '{{ geonames_username }}'
# Mapbox token shared with Winthrop
MAPBOX_ACCESS_TOKEN = '{{ mapbox_token }}'

DJIFFY_AUTH_TOKENS = {
    'plum.princeton.edu': '{{ plum_token }}',
    'figgy.princeton.edu': '{{ figgy_token }}',
}
# set compress offline for Django Compressor
COMPRESS_OFFLINE = True
# turn on google analytics
INCLUDE_ANALYTICS = True

{% endblock %}
