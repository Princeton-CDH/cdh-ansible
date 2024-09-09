# Role Name

Setup role to be used as a dependency for other roles. Includes the following:

- Conditionally load vaulted variables for setup tasks (geniza vault var; outdated)
- Configure NFS mount point when NFS is enabled
- Configure TigerData mount point when TigerData is enabled
- Install and configure rclone when `rclone_remotes` are configured

## Requirements

None

## Role Variables

Checks whether the `geniza_deploy_only` variable is defined to determine
whether to load setup vault variables.

### rclone

The `rclone` task will run if any `rclone_remotes` are defined.

This configuration takes a list of remotes with remote names `name` and
dictionary of options, to be put in the rclone config file.

For example, this set of ansible variables:

```
# rclone remote config
rclone_remotes:
  - name: "test_gdrive"
    options:
      type: "drive"
      scope: "drive"
```

Would result in this rclone configuration:

```
[test_gdrive]
type = drive
scope = drive
```

This task includes credentials for a Google service account. The service credentials file
will automatically be configured for any remotes with type `drive`. You must add the service account `cdh-gdrive@pul-gcdc.iam.gserviceaccount.com` to any folder you wish it to have access with appropriate permission for your planned usage (read/update).

To set a remote to a specific Google Drive folder, set the folder id as `root_folder_id`.

## Dependencies

None

## License

See [LICENSE](https://github.com/Princeton-CDH/CDH_ansible/blob/main/LICENSE).
