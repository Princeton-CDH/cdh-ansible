# Passenger

Borrowed from [pulibrary / princeton_ansible](https://github.com/pulibrary/princeton_ansible/tree/main/roles/passenger), who originally borrowed from Geerling Guy.

Installs Passenger (with Nginx) Ubuntu linux servers, with configuration
to serve wsgi application.

## Requirements

None.

## Role Variables

Application name variable ``app_name`` must be defined.

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
passenger_server_name: www.example.com
```

The server name (used in the Nginx virtual host configuration).

```yaml
passenger_app_root: /var/www/app
```

The wsgi file to use and the path to the python to use (i.e., if you need python within a virtualenv):

```yaml
passenger_startup_file: app/wsgi.py
passenger_python: /usr/bin/python
```

The nginx site configuration template to use, if you want to exstend it:

```yaml
passenger_nginx_site_template: passenger.conf.j2
```

Values for passenger configuration directives inside `nginx.conf`. These defaults should generally work correctly.

```yaml
nginx_worker_processes: "{{ ansible_processor_vcpus | default(ansible_processor_count) }}"
nginx_worker_connections: "768"
nginx_keepalive_timeout: "65"
nginx_remove_default_vhost: true
```

Nginx directives.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: server
    roles:
    - passenger
```

## License

See [LICENSE](https://github.com/Princeton-CDH/CDH_ansible/blob/main/LICENSE).


## Author Information

This role was originally created in 2015 by [Jeff Geerling](https://www.jeffgeerling.com/), author of [Ansible for DevOps](https://www.ansiblefordevops.com/); this version is adapted from [pulibrary / princeton_ansible](https://github.com/pulibrary/princeton_ansible/tree/main/roles/passenger); any changes are now managed locally.


