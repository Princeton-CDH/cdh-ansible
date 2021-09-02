django
======

Django tasks typically needed for configuring and running a Django application.brief description of the role goes here.  Currently includes tasks for running `collectstatic`, installing local settings, running migrations, and compiling messages; each task can also be called separately.

Requirements
------------

Assumes that the django application has already been checked out and is ready for configuration.

Role Variables
--------------

All variables have default values, although many of them are placeholders to simplify testing and are expected to be customized.

main config
^^^^^^^^^^^

- `django_app`: Name of the django application; default `myapp`
- `django_app_path`: Full path to the django application on the remote host; default `/srv/www/{{ django_app }}`
- `django_user`: User to use when runing django manage commands, default `ansible_user`
- `django_venv_path`: Path to python virtualenv, default `"{{ django_app_path }}/env`"

django settings config
^^^^^^^^^^^^^^^^^^^^^^
- `django_local_settings_template`: default `local_settings.py`; override if customization is needed
- `django_secret_key`: secret key for local settings; default `changeme`, please change
- `django_debug`: debug setting for local settings, default `false`
- `django_allowed_hosts`: list of allowed hosts for settings; default list is `localhost` and `ansible_hostname`
- `django_test_warning`: configuration for django show test warning; default `false`

database config
^^^^^^^^^^^^^^^
- `django_db_backend`: last portion of db backend for settings; default `postgresql`
- `django_db_name`: database name, default `django_app`
- `django_db_user`: database user, default `django_app`
- `django_db_host`: database server hostname, default `localhost`
- `django_db_password`: database password for user, default `changeme`,  please change

email config
^^^^^^^^^^^^
- `django_email_password`: configuration for **EMAIL_HOST_PASSWORD** in django settings, default `changeme`
- `django_email_subject`: configuration for **EMAIL_SUBJECT_PREFIX** in django settings, default `[{{ django_app }}]`

csp config
^^^^^^^^^^
Configuration for Content Security Policy reporting in django setttings

- `django_csp_reportonly_uri`: endpoint for reporting (QA); default `http://example.com/`
- `django_csp_enforce_uri`: endpoint for enforcing; default `http://example.com/`

Dependencies
------------

Depends on the **python** to install python binary and python packages.

Example Playbook
----------------


```yml
    - hosts: myapp
      roles:
         - { role: django.migrate, django_user: "conan" }
```
