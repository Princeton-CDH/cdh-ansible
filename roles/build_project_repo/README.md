# build_project_repo

An Ansible role to manage project repository deployments at CDH (PUL). This role performs a two-stage deployment: it maintains a primary clone of a repository and creates a versioned, shallow checkout for the active deployment.

## Features

- **Dual-Stage Deployment**: Maintains a persistent local clone in `clone_root` and a production-ready shallow checkout in `deploy`.

- **Git Security Compliance**: Automatically whitelists directories via `git config safe.directory` to prevent "dubious ownership" errors.

- **Python Versioning**: Optionally detects application versions using `_version.py` or package metadata.

- **Idempotency**: All Git and file operations are designed to skip work if the target state is already achieved.

- **Error Recovery**: Includes a rescue block to trigger deployment failure notifications.

## Role Variables

The role is designed to work seamlessly with the global variables defined in `inventory/group_vars/all/vars.yml`.

| **Variable**   | **Default**                                         | **Description**                                                       |
| -------------- | --------------------------------------------------- | --------------------------------------------------------------------- |
| `deploy_user`  | `conan`                                             | The remote user that owns the repository and deployment.              |
| `repo_url`     | `https://github.com/{{ repo }}.git`                 | The full URL to the GitHub repository.                                |
| `repo`         | `N/A`                                               | The repository name (e.g., `Princeton-CDH/derridas-margins-archive`). |
| `gitref`       | `main`                                              | The branch, tag, or commit hash to deploy.                            |
| `install_root` | `/srv/www/{{ app_name }}`                           | The base directory for application deployments.                       |
| `clone_root`   | `/home/{{ deploy_user }}/repos`                     | Where the primary Git clone is maintained.                            |
| `deploy`       | `{{ install_root }}/{{ version }}-{{ short_hash }}` | The final versioned path for the shallow checkout.                    |
| `python_app`   | `N/A`                                               | (Optional) The name of the Python package to check for versioning.    |

## Dependencies

- **`create_deployment`**: (Implicit) The role's rescue block attempts to include `roles/create_deployment/tasks/fail.yml` on failure.

## Example Playbook

YAML

```text
- hosts: all
  vars:
    app_name: "derrida"
    repo: "Princeton-CDH/derridas-margins-archive"
    python_app: "derrida"
  roles:
    - role: build_project_repo
```

## Internal Logic Flow

The following diagram illustrates how the role moves code from GitHub to your production directory while resolving the versioning dependencies:

1. **Preparation**: Ensures `install_root` and `clone_root` exist and are owned by `deploy_user`.

2. **Safety**: Adds the clone path to Git's `safe.directory` global config.

3. **Primary Clone**: Clones the repo to `clone_root` to register `repo_info`.

4. **Versioning**: Runs `python_app_version.yml` to set `python_app_version`.

5. **Shallow Checkout**: Performs a `git checkout` from the local clone into the final versioned `deploy` directory.

## Testing with Molecule

To run the generalized test suite:

Bash

```text
# Set platform for Apple Silicon if necessary
export MOLECULE_DOCKER_PLATFORM=linux/arm64 

molecule converge
molecule verify
```

The verify step ensures that both the clone and deploy directories exist, have correct ownership, and are recognized as valid Git repositories by the `deploy_user`.
