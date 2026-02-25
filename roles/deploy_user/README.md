# deploy_user

This role manages the creation and configuration of a dedicated deployment user (default: `conan`). It ensures the user is properly provisioned with the necessary group memberships, shell environment, and SSH configurations required for automated deployments.

## Features

- **User & Group Provisioning**: Creates a system user and matching group with a specific UID/GID for cross-node consistency.

- **Webserver Integration**: Automatically adds the deploy user to the `webapp_group` (e.g., `www-data`) to ensure write access to logs and shared assets.

- **Automated SSH Key Management**:

  - Distributes a master private key from the control machine (optional).

  - Idempotently generates a local SSH key pair if one does not exist.

  - Configures `authorized_keys` with the control machine's public key.

- **Hardened SSH Access**: Modifies `sshd_config` to explicitly allow the deploy user and ensures `AuthorizedKeysFile` is correctly configured.

- **Developer Experience**:

  - Deploys a `.profile` (bash profile) with automated virtualenv activation (the `activate` alias).

  - Adds a `.bash_aliases` file for the `ansible_user` (e.g., `pulsys`) to allow quick `sudo su -` access to the deploy user.

## Variables

| **Variable**              | **Default** | **Description**                                                        |
| ------------------------- | ----------- | ---------------------------------------------------------------------- |
| `deploy_user`             | `conan`     | The name of the deployment user.                                       |
| `deploy_user_uid`         | *Required*  | The UID for the user (must match GID).                                 |
| `deploy_user_shell`       | `/bin/bash` | Default shell for the user.                                            |
| `webapp_group`            | `www-data`  | The webserver group on the target system.                              |
| `single_app`              | `true`      | If true, the bash profile defaults to activating a single environment. |
| `python_venv_path_prefix` | `""`        | Optional prefix for the Python virtual environment path.               |

## SSH Configuration Details

This role ensures that the deployment user is ready for cross-server tasks (such as `rsync` delegation between an application server and a Solr server). It uses the `ansible.builtin.user` module to generate keys, ensuring that every managed node has a unique identity for "calling home" to other nodes in the cluster.

### Security Note

The role modifies `/etc/ssh/sshd_config` to use `AllowUsers`. If you have existing users that require SSH access, ensure they are accounted for in your global variables, or they may be locked out.

## Example Playbook

```yaml
- hosts: all
  become: true
  roles:
    - role: deploy_user
      vars:
        deploy_user: conan
        deploy_user_uid: 1001
```

## Idempotency & Process Conflicts

If the role fails during user modification (`rc: 8`), it is likely because the `conan` user has active SSH or `rsync` processes. Ensure background processes are terminated before attempting to change the UID or primary group of an existing user.
