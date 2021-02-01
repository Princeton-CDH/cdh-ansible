{% extends "settings.py" %}
"""
Django settings for geniza i18n prototype.
"""

{% block cas_config %}
CAS_SERVER_URL = "https://fed.princeton.edu/cas/"

CAS_VERSION = "CAS_2_SAML_1_0"

PUCAS_LDAP = {
    "ATTRIBUTES": ["givenName", "sn", "mail"],
    "ATTRIBUTE_MAP": {
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail",
    },
    "SERVERS": [
        "ldap2.princeton.edu",
        "ldap3.princeton.edu",
        "ldap4.princeton.edu",
        "ldap5.princeton.edu"
    ],
    "SEARCH_BASE": "o=Princeton University,c=US",
    "SEARCH_FILTER": "(uid=%(user)s)",
}
{% endblock %}

{% block extra_config %}
STATIC_URL = "{{ apache_app_url }}/static/"
{% endblock %}