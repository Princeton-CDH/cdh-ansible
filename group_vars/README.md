# group_vars

## `all/`

This contains two files `vars.yml` for open variables shared by all deploys and
`vault.yml`, which is an encrypted file that holds sensitive variables (i.e.
database names, passwords, users, etc.)

## `vault.yml`

This file can be encrypted/decrypted using `ansible vault edit`. It can also
be edited with `ansible vault decrypt` but this requires a manual `ansible
vault encrypt` and is not recommended.

All variables are named spaced `vault_playbook_var_name` and referenced in
unencrypted `group_vars` YAML files.
