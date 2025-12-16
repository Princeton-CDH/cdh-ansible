# Passenger

This role installs and configures Nginx with Phusion Passenger, specifically optimized for serving Python WSGI applications (such as Django). It handles the setup of the Phusion Passenger apt repository, GPG key management (including the 2025 key rotation), and virtual host configuration.

## Requirements

* **OS**: Debian/Ubuntu based systems (due to `apt` module usage).
* **Root Access**: The role requires `become: true` for installation tasks.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

### Application Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `passenger_server_name` | `www.example.com` | The domain name for the Nginx server block. |
| `passenger_app_root` | `/var/www/app` | The root directory of the application. |
| `passenger_startup_file` | `wsgi.py` | The entry point file for the WSGI application. |
| `passenger_python` | `/usr/bin/python` | Path to the Python interpreter (e.g., inside a virtualenv). |
| `passenger_site_config_name` | `{{ app_name }}` | Filename for the Nginx site configuration in `sites-available`. |
| `passenger_enabled` | `on` | Toggles Passenger support for the location. |
| `deploy_env_vars` | *undefined* | A dictionary of environment variables to pass to the application (e.g., `SECRET_KEY`). |

### Nginx Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `passenger_listen_port` | `'80'` | Port Nginx should listen on. |
| `nginx_max_body_size` | `50M` | Maximum allowed size of the client request body. |
| `nginx_worker_processes` | `vcpus` or `count` | Number of worker processes (defaults to auto-detect). |
| `nginx_worker_connections` | `768` | Maximum number of simultaneous connections per worker. |
| `nginx_keepalive_timeout` | `65` | Timeout for keep-alive connections. |
| `nginx_remove_default_vhost`| `true` | Whether to remove the default 'Welcome to Nginx' site. |
| `nginx_user` | `{{ __nginx_user }}` | System user Nginx runs as (detected via OS vars). |

### Static Files & Media

| Variable | Default | Description |
|----------|---------|-------------|
| `passenger_static_path` | `{{ passenger_app_root }}/static/` | Path to serve static files from `/static/`. |
| `media_root` | `/var/www/media/` | Path to serve user-uploaded media from `/media/`. |
| `font_path` | `/var/www/fonts/` | Path to serve fonts from `/static/fonts/`. |
| `font_require_referrer` | `[]` | List of valid referrers for font access (hotlink protection). |

### Templates & customization

| Variable | Default | Description |
|----------|---------|-------------|
| `passenger_nginx_site_template` | `passenger.conf.j2` | The Jinja2 template used for the site config. |
| `passenger_extra_config` | `''` | Raw Nginx config string appended to the server block. |

## Dependencies

This role relies on OS-specific variables (loaded via `include_vars`) to define `nginx_passenger_packages`. Ensure your `vars/` directory contains the appropriate package lists for Ubuntu (e.g., `nginx-extras`, `passenger`, `libnginx-mod-http-passenger`).

## Features

### Repository & Key Management

The role automatically handles the Phusion Passenger GPG keys:

* Installs the **Legacy Key** (SHA1) for backward compatibility.
* Installs the **2025 Future-Proof Key** (SHA256) for newer repositories.
* Converts keys to the modern GPG keyring format (`/usr/local/share/keyrings`) and installs them into `/etc/apt/trusted.gpg.d/`.

### Monitoring

* Enables the `stub_status` module at `/nginx_status`.
* Access is restricted to `127.0.0.1` (localhost) only, suitable for agents like Datadog.

## Example Playbook

```yaml
- hosts: webservers
  roles:
    - role: passenger
      vars:
        app_name: "my_django_app"
        passenger_server_name: "app.example.com"
        passenger_app_root: "/opt/django/my_app"
        passenger_python: "/opt/django/venv/bin/python"
        passenger_startup_file: "wsgi.py"
        deploy_env_vars:
            DATABASE_URL: "postgres://user:pass@localhost/db"
            SECRET_KEY: "supersecret"
```
