# Cryptographic key for signing secrets. Keep the production key hidden!
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = "{{ django_secret_key }}"

# Display detailed error messages. Turn off in production!
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = {{ django_debug }}

# Valid hostnames this site can serve.
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [{% for host in django_allowed_hosts %}"{{ host }}", {% endfor %}]

# Use x-forwarded-proto header to tell if request from nginx was https or not
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Show a small "this is a test site" banner for QA sites, if corresponding
# template and stylesheet are present.
SHOW_TEST_WARNING = {{ django_test_warning }}

{% if media_root is defined %}
# Configure media root path
MEDIA_ROOT = '{{ media_root }}'
{% endif %}

# Database configuration
# https://docs.djangoproject.com/en/dev/ref/databases/
{% block db_config %}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.{{ django_db_backend }}",
        "NAME": "{{ django_db_name }}",
        "USER": "{{ django_db_user }}",
        "PASSWORD": "{{ django_db_password }}",
        "HOST": "{{ django_db_host }}",
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
{% block logging_config %}
# Solution following https://stackoverflow.com/a/9541647
# Sends a logging email even when DEBUG is on
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'basic': {
            'format': '[%(asctime)s] %(levelname)s:%(name)s::%(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },
        # This configuration lets logrotate and its proper permissions #
        # handle this problem #
        'debug_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '{{ django_logging_path }}',
            'formatter': 'basic',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'debug_log'],
            'level': 'ERROR',
            'propagate': True,
        },
        '{{ django_app }}': {
            'handlers': ['debug_log'],
            'level': {% if qa is defined %}'DEBUG'{% else %}'WARN'{% endif %},
            'propagate': True,
        },
    }
}
{% endblock %}

# Solr configuration (search index)
# https://github.com/Princeton-CDH/parasolr
{% block solr_config %}
{% if solr_url is defined %}
SOLR_CONNECTIONS = {
    'default': {
        'URL': '{{ solr_url }}',
        'COLLECTION': '{{ solr_collection }}',
        'CONFIGSET': '{{ solr_configset }}'
    }
}
{% endif %}
{% endblock %}

# Extra app-specific configuration
{% block extra_config %}{% endblock %}
