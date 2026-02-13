# Supervisor (Ubuntu)

An Ansible Role that and installs and configures [Supervisor](http://supervisord.org/) specifically on **Ubuntu** using `pip`. This role is a geerlingguy refactored to remove legacy init scripts and RedHat support, favoring a streamlined `systemd` implementation.

## Features

- **Pip-based installation**: Installs the latest (or specific) version of Supervisor via Python's package manager.

- **Systemd integration**: Configures a native systemd unit file for modern Ubuntu (20.04, 22.04, 24.04).

- **Program Management**: Easily define and manage multiple processes via Ansible variables.

- **Ubuntu Only**: Stripped of cross-distro complexity for faster execution and easier maintenance.

## Role Variables

Available variables are listed below with their default values (see `defaults/main.yml`):

### Installation Settings

- `supervisor_version`: `''`

  Install a specific version of Supervisor (e.g., `'4.2.5'`). If left empty, the latest version is installed.

- `supervisor_started`: `true`

  Whether the `supervisord` service should be running.

- `supervisor_enabled`: `true`

  Whether the service should start on boot.

### Paths

- `supervisor_config_path`: `/etc/supervisor`

  Where `supervisord.conf` and `conf.d/` will reside.

- `supervisor_log_dir`: `/var/log/supervisor`

  The location for Supervisor's internal logs.

### Authentication & UI

- `supervisor_user`: `root`

- `supervisor_password`: `'change_me'`

  Used for both the UNIX socket (`supervisorctl`) and the optional Inet HTTP server.

### Managed Programs

The `supervisor_programs` list allows you to define the processes you want Supervisor to manage.

YAML

```text
supervisor_programs:
  - name: 'my-app'
    command: /usr/bin/python3 /opt/app/main.py
    state: present
    configuration: |      autostart=true      autorestart=true      user=www-data      stdout_logfile=/var/log/my-app.out.log
```

## Dependencies

None

## Example Playbook

YAML

```text
- hosts: servers
  become: true
  roles:
    - role: pulibrary.supervisor
      vars:
        supervisor_programs:
          - name: 'worker'
            command: /usr/local/bin/worker-script.sh
            state: present
```

## Testing with Molecule

This role includes a Molecule test suite configured for Ubuntu 22.04.

Bash

```text
# Run the full test suite
uv run molecule test

# Run just the convergence and verify steps
uv run molecule converge
uv run molecule verify
```

## License

MIT
