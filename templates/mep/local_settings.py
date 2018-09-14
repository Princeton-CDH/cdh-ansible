{% extends 'templates/common/base.py' %}

{% block extra_config %}
{# Add static root as needed now because missing from settings.py as of 0.7 #}
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
{% endblock %}
