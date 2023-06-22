{% extends 'local_settings.py' %}

{% block extra_config %}
# Media settings for running under apache in production and QA
MEDIA_ROOT = '{{ media_root }}'
MEDIA_URL = '/media/'

# Email address for a technical contact.
TECHNICAL_CONTACT = '{{ technical_contact }}'

# Set local path to HathiTrust pairtree data provided via rsync
HATHI_DATA = '{{ hathitrust_pairtree_path }}'

# Email address for a technical contact.
# Will be used in From header for HathiTrust API requests
TECHNICAL_CONTACT = '{{ technical_contact }}'

GALE_API_USERNAME = '{{ gale_api_username }}'

# local path for cached marc records; needed for Gale/ECCO import
MARC_DATA = '{{ marc_data_path }}'

{% if qa is not defined %}
# Turn on Google Analytics
INCLUDE_ANALYTICS = True
GTAGS_ANALYTICS_ID = 'G-FJG5ZQ5KGR'
{% endif %}

{% endblock %}