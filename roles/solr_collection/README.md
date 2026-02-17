# solr_collection

This role manages the creation and configuration of Solr collections and configsets within a SolrCloud environment. It handles the synchronization of local configuration files to remote Solr servers and their subsequent upload to ZooKeeper.

## Features

- **Configset Management**: Uses `rsync` with checksum verification to idempotently sync Solr configurations.

- **ZooKeeper Integration**: Automatically uploads/updates configsets to ZooKeeper using the Solr CLI.

- **Collection Lifecycle**: Idempotently creates collections and manages replication factors/shards.

- **Cross-Server Delegation**: Designed to run from an application server while delegating infrastructure tasks to a Solr/Zookeeper node.

## Role Variables

| **Variable**         | **Default** | **Description**                                                      |
| -------------------- | ----------- | -------------------------------------------------------------------- |
| `solr_server`        | *Required*  | The FQDN of the Solr node (e.g., `lib-solr-staging2.princeton.edu`). |
| `solr_collection`    | *Required*  | The name of the collection to manage.                                |
| `solr_configset`     | *Required*  | The name of the configset in ZooKeeper.                              |
| `num_shards`         | `1`         | Number of shards for the collection.                                 |
| `replication_factor` | `3`         | Number of replicas per shard.                                        |
| `deploy_user`        | `conan`     | The user who owns the config files and performs the sync.            |

## Workflow Diagram

The role follows this logic to ensure idempotency:

1. **Sync**: Rsyncs local `solr_conf` to the `solr_server`.

2. **Detect**: Checks if any files actually changed (using checksums).

3. **Upload**: Updates ZooKeeper only if changes were detected or the configset is missing.

4. **Create**: Issues a `CREATE` call only if the collection does not appear in the Solr `LIST` API.

## Dependencies

- **`setup`**: This role must run first to ensure the `deploy_user` and SSH `authorized_keys` exist on the `solr_server`.

## Example Playbook


```yaml
- hosts: app_servers
  roles:
    - role: solr_collection
      vars:
        solr_server: lib-solr-staging2.princeton.edu
        solr_collection: geniza_production
        solr_configset: geniza_conf
        num_shards: 2
```

## Troubleshooting

### Rsync Permission Denied

If the `rsync` task fails, ensure that:

1. The `setup` role has run against the `solr_server`.

2. The `conan` user on the `solr_server` has the corresponding private key to match the `authorized_keys` on the application server, or that SSH agent forwarding is active.

### ZooKeeper Failures

The role assumes Solr is installed at `/opt/solr`. If your installation path differs, override the path in the `zk upconfig` task.
