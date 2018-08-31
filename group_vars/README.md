# group_vars

## Group var folders

These contain two files `vars.yml` for open variables and
`vault.yml`, which is an encrypted file that holds sensitive variables (i.e.
database names, passwords, users, etc.)

## `vault.yml`

These files can be encrypted/decrypted using `ansible-vault edit`. It can also
be edited with `ansible-vault decrypt` but this requires a manual `ansible-vault
encrypt` and is not recommended.

All variables are named spaced `vault_var_name` and referenced in
unencrypted `vars.yml` files.

## Folder structure
The folder structure uses Ansible groups (defined in `hosts`) to include common
variables as needed (which can then be overridden): The general inheritence is
as follows:

- all
  - staging
  - project
    - project_qa
    - project_prod
    - project_staging

In hosts, `project_staging` inherits from both its project and `staging`, so database variables do not have to be defined for staging playbooks.
