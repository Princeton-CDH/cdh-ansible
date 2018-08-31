# CDH Ansible Repository

## Overall structure

The overall structure of this repository can be broken down as follows:
  - `roles` - the various tasks that Ansible can perform in a group.
  - `group_vars` - the group variables for different deploys
    - `all` - any variables shared by all deploys
      - `vars.yml`- unencrypted all variables
      - `vault.yml` - `ansible vault` encrypted variables
    - Individual project group variables
  - `templates` - templated files under folder named by group
  - `hosts` - host file with groups and their associated host(s)
  - top level YAML files for different groups.

## Using these playbooks

### Requirements
  - Virtual environment with Ansible 2.4+ installed.
    - If you use `env`, the `.gitignore` will automatically exclude it.
  - The CDH Ansible vault key. This can be referenced on the command line or
  better set as in the Bash session, i.e.
  `export ANSIBLE_VAULT_PASSWORD_FILE=/path/to/.passwd`
  - The CDH deploy bot key. This can be added to ssh-agent or in `~/.ssh/config`.
  All production deploys must be on the campus network (including VPN) and
  proxy through the QA server to production, with an ssh config stanza
  that looks something like:
  ```
  Host derridas-margins.princeton.edu
      User deploy
      Proxycommand ssh QASERVERHOST -W %h:%p
      Identityfile ~/.ssh/deploy_key
  ```

### Running a playbook

To run a playbook, from your virtual environment, simply invoke:

```{bash}
ansible-playbook name_of_playbook.yml
```

QA playbooks should point by default to the develop branch and production playbooks
(denoted by an absence of `_qa` suffix) to master.

To deploy a different reference (hash, tag, or branch), use the syntax:

```{bash}
ansible-playbook -e ref=GITREF name_of_playbook.yml
```

The playbook will run, noting success and failures. The `-v` flag adjusts verbosity
(adding more `v`s will produce more verbosity. Debug tasks are usually written at `2`)

## Vault variables

Variables kept in `group_vars/all/vault.yml` are sensitive configurations
that should always be kept encrypted on commit. To edit them (in your system
text editor):
```{bash}
ansible-vault edit group_vars/all/vault.yml
```

You can also `ansible-vault decrypt` but need to remember to manually `encrypt`.

All vault variables should be prefixed with `vault_playbookname_` to keep them
identifiable and unique.

These are included in playbooks indirectly. Typically in the appropriate
`group_vars` YAML file, you'll see a stanza such as:
```{yaml}
db_name: ^^ vault_winthrop_db_name ^^
```

These use either the standard `{{}}` or alternate `^^ ^^` tags to denote
printing the referenced vault variable. This aliases the appropriate variable
in the vault to its more generic name used in the roles.

N.B. The `^^` avoids an issue in the `install_local_settings` role where `{}`
  are interpreted as Jinja2 templating commands, not valid Python. For the
  duration of that role, the Jinja2 print braces are `^^ myvar ^^`. This
  alternate form needs to be used for ANY variable referenced in
  `local_settings.py` in Django-based projects.

## Adding a playbook

The rough order of creating a playbook is:

  1. Copy over an appropriate playbook as a template that is either production
  or QA.
  2. Create a group in hosts (QA and production
    are or should be separate):
    ```
    [mygroup]
    hostname.of.server.edu
    ```
  3. Create a YAML directory in `group_vars` that has a name mirroring the new
  playbook: i.e. if the playbook is `my_playbook_qa`, the name should be
  the same, with a `vars.yml` and a `vault.yml` (for encrypted variables) included
  4. Reference any playbook variables and set accordingly. See above under
  vault variables for how to configure those.
  5. Add roles to the list in the new playbook in the order needed.
  6. N.B. Make sure you set the `group_name` variable appropriately as some QA
  only steps are skipped based on `_qa` not being in the name.

## Staging playbooks

These are adaptable playbooks (which can either be aimed at production or a
future production release currently in a branch/develop), that require a running
instance of the staging vagrant VM running with SSH on port 2222.

To configure this, after you have installed [Vagrant](https://www.vagrantup.com/downloads.html)
and [VirtualBox](https://www.virtualbox.org/wiki/Downloads)from the `CDH_ansible/vagrant` directory,
run `vagrant up`. This will take
considerable time the first run, but will download a Centos 7 box, provision it
with the necessary packages to emulate production VMs, and set up expected
settings that Puppet manages on the production VMs.

For detailed info on the VM and its accounts, configuration, especially how to
set up Solr (since deploys do not yet touch it), see the `vagrant` directory
[README](vagrant/README.md).
