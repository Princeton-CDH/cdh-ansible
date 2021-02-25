{% extends "settings.py" %}
"""
Django settings for geniza
"""

{% block database %}
DATABASES = {
    'default': {
        'ENGINE': 'psqlextra.backend',
        'NAME': '{{ db_name }}',
        'USER': '{{ db_username }}',
        'PASSWORD': '{{ db_password}}',
        'HOST': '{{ db_host }}',
        'PORT': '',
    }
}
{% endblock %}

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
# Use x-forwarded-proto header to tell if request from nginx was https or not
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# urls to google sheets data published as csv for import
DATA_IMPORT_URLS = {
    'libraries': '{{ libraries_csv_url }}',
    'languages': '{{ languages_csv_url }}',
    'metadata': '{{ metadata_csv_url }}'
}
{% endblock %}