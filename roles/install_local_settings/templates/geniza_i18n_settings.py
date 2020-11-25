{% extends 'settings.py' %}
"""
Django settings for geniza i18n prototype.
"""

{% block cas_config %}
{% endblock %}

{% block extra_config %}
STATIC_URL = "{{ apache_app_url }}/static/"
{% endblock %}