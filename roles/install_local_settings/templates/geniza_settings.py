{% extends "settings.py" %}
"""
Django settings for geniza
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
{% endblock %}