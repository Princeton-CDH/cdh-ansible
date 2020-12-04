{% block basic_settings %}
DEBUG = {{ debug_setting }}

ALLOWED_HOSTS = [{% for host in allowed_hosts %}'{{ host }}', {% endfor %}]

# SECURITY WARNING: keep the secret key used in production secret!
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = '{{ secret_key }}'

{# only show the test warning if in QA #}
{% if qa is defined %}
SHOW_TEST_WARNING = True
{% endif %}

{% endblock %}

{% block database %}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{{ db_backend }}',
        'NAME': '{{ db_name }}',
        'USER': '{{ db_username }}',
        'PASSWORD': '{{ db_password}}',
        'HOST': '{{ db_host }}',
        'PORT': '',
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci',
        {% if db_backend == "mysql" %}
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
        {% endif %}
    },
}
{% endblock %}

{% block cas_config %}
CAS_SERVER_URL = 'https://fed.princeton.edu/cas/'

CAS_VERSION = 'CAS_2_SAML_1_0'

PUCAS_LDAP.update({
    'SERVERS': [
        'ldap2.princeton.edu',
        'ldap3.princeton.edu',
        'ldap4.princeton.edu',
        'ldap5.princeton.edu'
    ],
    'SEARCH_BASE': 'o=Princeton University,c=US',
    'SEARCH_FILTER': "(uid=%(user)s)",
    # other ldap attributes we might want:
    # ou = organizational unit
})
{% endblock %}

{% block solr_config %}{% endblock %}

{% block email_config %}
# Admin email settings for error messages
ADMINS = [('CDH Dev Team', 'cdhdevteam@princeton.edu')]
SERVER_EMAIL = 'cdhdevteam@princeton.edu'
# Email settings for wagtail: see
# https://docs.wagtail.io/en/latest/reference/settings.html#email-notifications
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = SERVER_EMAIL
WAGTAILADMIN_NOTIFICATION_USE_HTML = True

{% if qa is not defined %}
# Email configuration for sending messages
EMAIL_HOST = 'smtp.princeton.edu'
EMAIL_HOST_USER = 'cdhdevteam'
EMAIL_HOST_PASSWORD = '{{ email_host_password }}'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
{% endif %}
EMAIL_SUBJECT_PREFIX = '{{ email_prefix }}'


{% endblock %}

{% block csp %}

{% if csp_enabled is defined and csp_enabled %}

{% if qa is defined %}
CSP_REPORT_ONLY = True
CSP_REPORT_URI = '{{ csp_reportonly_uri }}'
{% else %}
CSP_REPORT_URI = '{{ csp_enforce_uri }}'
{% endif %}

{% endif %}
{% endblock %}

{% block logging %}{% endblock %}

{% block extra_config %}{% endblock %}
