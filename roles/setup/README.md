# setup

This role performs foundational system configuration for CDH infrastructure. It is primarily used as a dependency for other roles (like `solr_collection` or `deploy_user`) to ensure the environment is consistent across application and infrastructure servers.

## Features

- **User & Group Provisioning**: Ensures the `deploy_user` (default: `conan`) exists and belongs to the correct system groups.

- **SSH Access**: Manages idempotent distribution of SSH public keys to allow cross-server communication (e.g., `rsync` between app and Solr servers).

- **NFS Mounts**: Conditionally configures standard CDH and TigerData NFS mount points.

- **Rclone Installation**: Installs and configures `rclone` for cloud storage interactions.

- **Vault Integration**: Automatically loads sensitive variables if `geniza_deploy_only` is not set.

## Role Variables

### General

| **Variable**        | **Default** | **Description**                                                    |
| ------------------- | ----------- | ------------------------------------------------------------------ |
| `deploy_user`       | `conan`     | The system user responsible for deployments and service ownership. |
| `nfs_enabled`       | `true`      | Whether to attempt mounting standard NFS shares.                   |
| `tigerdata_enabled` | `false`     | Whether to attempt mounting TigerData-specific NFS shares.         |

### Rclone

The `rclone` tasks trigger if `rclone_remotes` is defined.

```yaml
rclone_remotes:
  - name: "test_gdrive"
    options:
      type: "drive"
      scope: "drive"
```

## Cross-Server Communication (Rsync)

This role is critical for tasks that use `delegate_to`. By ensuring the `deploy_user` and their `authorized_keys` are present on the delegated host, it allows for passwordless `rsync` operations.

> [!IMPORTANT]
> 
> This role uses `exclusive: no` for SSH keys. This means Ansible will ensure your deployment keys are present without deleting manually added administrator keys.

## Dependencies

None. This is intended to be a "base" role.

## Usage as a Dependency

In your role's `meta/main.yml`:

```yaml
dependencies:
  - role: setup
    vars:
      tigerdata_enabled: true
```

## Idempotency Notes

- **Users/Groups**: Uses the native `ansible.builtin.user` and `group` modules.

- **NFS**: Uses `ansible.posix.mount` to ensure shares are in `/etc/fstab` and mounted without re-mounting on every run.

- **Vault**: Variables are conditionally loaded to prevent "Missing Vault Password" errors during limited deployment runs.
