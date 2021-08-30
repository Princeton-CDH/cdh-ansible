# Cryptographic key for signing secrets. Keep the production key hidden!
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = "{{ django_secret_key }}"

# Display detailed error messages. Turn off in production!
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = {{ django_debug }}

# Valid hostnames this site can serve.
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [{% for host in django_allowed_hosts %}"{{ host }}", {% endfor %}]

# Show a small "this is a test site" banner for QA sites, if corresponding
# template and stylesheet are present.
SHOW_TEST_WARNING = {{ django_test_warning }}

# Database configuration
# https://docs.djangoproject.com/en/dev/ref/databases/
{% block db_config %}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.{{ django_db_backend }}",
        "NAME": "{{ application_db_name }}",
        "USER": "{{ application_dbuser_name }}",
        "PASSWORD": "{{ application_dbuser_password }}",
        "HOST": "{{ application_db_host }}",
        "CHARSET": "utf8",
        "COLLATION": "utf8_general_ci",
        {% if django_db_backend == "mysql" %}
        "OPTIONS": {
            "init_command": "SET sql_mode="STRICT_TRANS_TABLES"",
        }
        {% endif %}
    },
}
{% endblock %}

# Princeton CAS configuration (authentication, user account creation)
# https://github.com/Princeton-CDH/django-pucas
{% block cas_config %}
CAS_SERVER_URL = "https://fed.princeton.edu/cas/"
CAS_VERSION = "3"
PUCAS_LDAP.update({
    "SERVERS": [
        "ldap2.princeton.edu",
        "ldap3.princeton.edu",
        "ldap4.princeton.edu",
        "ldap5.princeton.edu"
    ],
    "SEARCH_BASE": "o=Princeton University,c=US",
    "SEARCH_FILTER": "(uid=%(user)s)",
})
{% endblock %}

# Email configuration (error messages, admin notifications)
# https://docs.djangoproject.com/en/dev/howto/error-reporting/
# https://docs.wagtail.io/en/latest/reference/settings.html#email-notifications
{% block email_config %}
ADMINS = [("CDH Dev Team", "cdhdevteam@princeton.edu")]
SERVER_EMAIL = "cdhdevteam@princeton.edu"
{% if qa is not defined %}
EMAIL_HOST = "smtp.princeton.edu"
EMAIL_HOST_USER = "cdhdevteam"
EMAIL_SUBJECT_PREFIX = "{{ django_email_subject }}"
EMAIL_HOST_PASSWORD = "{{ django_email_password }}"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
{% endif %}
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = SERVER_EMAIL
WAGTAILADMIN_NOTIFICATION_USE_HTML = True
{% endblock %}

# Content-Security-Policy configuration (security)
# https://github.com/mozilla/django-csp
{% block csp_config %}
{% if csp_enabled is defined and csp_enabled %}
{% if qa is defined %}
CSP_REPORT_ONLY = True
CSP_REPORT_URI = "{{ django_csp_reportonly_uri }}"
{% else %}
CSP_REPORT_URI = "{{ django_csp_enforce_uri }}"
{% endif %}
{% endif %}
{% endblock %}

# Logging configuration
# https://docs.djangoproject.com/en/dev/topics/logging/
{% block logging_config %}{% endblock %}

# Solr configuration (search index)
# https://github.com/Princeton-CDH/parasolr
{% block solr_config %}{% endblock %}

# Extra app-specific configuration
{% block extra_config %}{% endblock %}
