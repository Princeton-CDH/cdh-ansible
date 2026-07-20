# Variables

Ansible variables in cdh-ansible are managed in three places: role defaults, inventory, and run-time overrides. The most complicated and most important to understand is host and group variables managed as part of the inventory.

## Inventory group variables

Groups are defined in `inventory/all_hosts` (see [host inventory](<inventory>)). Variables corresponding to these groups
are managed in folders under `inventory/group_vars/`.

cdh-ansible uses [nested groups](https://docs.ansible.com/projects/ansible/latest/inventory_guide/intro_inventory.html#grouping-groups-parent-child-group-relationships) to organize hosts and share variables where possible.

Each application has a staging and production environment, which are grouped in a parent app group:

```yaml
[app_staging]
test-app1.example.com

[app_production]
app1.example.com

[app:children]
app_staging
app_production
```

The staging and production groups are also included into environment-specific groups:

```yaml
[prod:children]
app_production
...

[staging:children]
app_staging
...
```

### Shared variables 

We use the built-in default **all** host group (`inventory/group_vars/all/`) for common, default production variables used across hosts (e.g., default deploy directory structure and paths). Common vaulted variables for all include shared credentials like the postgres admin password, which is used to provision and manage application databases and database users.

For hosts in the staging groups, these are overridden with staging-specific configurations in `inventory/group_vars/staging/`, e.g. replacing production service urls with staging equivalents (postgres, solr, NFS, etc).

For each application group, we define the majority variables in the main application group, and then override with environment specific configurations for the app_staging and app_production variables where necessary.  Since `app_staging` inherits from both its app group and `staging`, database variables typically do not need to be customized for staging.


The general inheritance order for a production host is as follows:
```
- all
  - app
    - app_production
```

And for a staging host:
```
- all
  - staging 
  - app
    - app_staging
```

To review the combined set of variables for a single machine, use `ansible-inventory`, e.g.:

```console
ansible-inventory --host cdh-test-prosody1.princeton.edu
```

### Vaulted variables

Configurations that are sensitive, such as passwords or API keys, should be
stored in a vault variable file (i.e., `inventory/group_vars/*/vault.yml`) and the **value** of the variable should be encrypted (but not the entire file). For compatibility with Ansible Tower, which loads group variables into inventory, we [encrypt individual variables](https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#encrypting-individual-variables-with-ansible-vault) rather than the entire vault.yml file.

To encrypt a single variable, you can use `ansible-vault`:

```sh
uv run ansible-vault encrypt_string <password_source> '<string_to_encrypt>' --name '<string_name_of_variable>'
```

To work with multiple encrypted variables, use the local `vault_vars.py` helper script.

- If all variables in a vault file are unencrypted, use `encrypt` mode to encrypt them
- To view the values of your vaulted variables, use the `decrypt` mode (does not replace content or preserve content)
- To check that all variable values in a vault file are encrypted use `check`

Example usage:

```sh
uv run bin/vault_vars.py encrypt inventory/group_vars/all/vault.yml
uv run bin/vault_vars.py decrypt inventory/group_vars/all/vault.yml
uv run bin/vault_vars.py check inventory/group_vars/all/vault.yml
```

The check mode of this script is used as a pre-commit hook to prevent sensitive
configurations from being checked into version control in plain text.

Refer to [ADR 005](<adr/0005-vault-variables-instead-of-files>) for the documented rationale for adopting this approach.
