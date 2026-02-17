# build_dependencies

This role installs the foundational system packages and utilities required across the CDH infrastructure. It is typically a dependency for more specific roles like `deploy_user` or `django`.

## Features

* **Package Management**: Standardizes the installation of common build tools, libraries, and Python environment essentials.
* **Cache Optimization**: Idempotently manages the `apt` cache to ensure updates are only performed when necessary.
* **System Utilities**: Deploys global configurations for tools like `tmux` to improve the developer/admin experience.

## Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `common_dependencies` | (List) | A base list of packages (git, curl, build-essential, etc.) installed on all hosts. |
| `app_dependencies` | `[]` | An empty list intended to be overridden in host/group vars or role calls for project-specific packages. |

## Usage

### Overriding Dependencies
To add specific system libraries for a project (e.g., PostgreSQL client or ImageMagick), pass them in your playbook:

```yaml
- hosts: app_servers
  roles:
    - role: build_dependencies
      vars:
        app_dependencies:
          - libpq-dev
          - imagemagick
```

### Idempotency
This role is fully idempotent.

  * Apt: Uses `cache_valid_time: 3600` to prevent redundant apt-get update calls on repeated runs.

  * Tmux: The configuration file is only updated if the source `tmux.conf` in the role differs from the one on the target system.
