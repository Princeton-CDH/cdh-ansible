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
      Proxycommand ssh deploy@QASERVERHOST -W %h:%p
      Identityfile ~/.ssh/key_for_qa_server
  ```

  And for deploying to the QA server:
  ```
  Host test-*.cdh.princeton.edu
      User deploy
      Identityfile ~/.ssh/key_for_qa_server
  ```

### Precommit hook
If you plan to contribute to this repository (i.e., you're a member of the CDH
dev team editing our playbooks), please copy the following in your local instance:

```{bash}
cp hooks/pre-commit .git/hooks/
```
This will add a simple pre-commit hook that will prevent you from commiting a
file with an uncrypted `vault.yml`. It isn't terribly smart in terms of looking
for secrets in a `local_settings.py`, but prevents worst case scenarios from
emerging.


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


## Overrides

There are two principal overrides that the roles involved in deployment have
built-in. One is the override noted above for
what Git reference should be used to deploy.
This can be any hash, branch head, or tag that the Git repository knows about.

You can also override any other arbitrary variable, but the other likely one
is the `requirements` file. You may want to point to a `requirements.lock`,
for example:
```{bash}
ansible-playbook -e requirements_type=lock playbook.yml
```

You can also pass a list of arbitrary additions or updates to pip:
```{bash}
ansible-playbook -e pip_updates='["django-autcomplete-light<3.3", "pandas"]' playbook.yml
```

These will be automatically added (or updated) to the requirements for the
application during its deployment.

If you need to make major changes and do not wish to make a patch release for
whatever reason, you can also entirely replace `requirements.(txt|lock)` with a
local template:

```{bash}
ansible-playbook -e new_requirements=/path/to/local/template.txt playbook.yml
```

## Vault variables

Variables kept in `group_vars/*/vault.yml` are sensitive configurations
that should always be kept encrypted on commit. To edit them (in your system
text editor):
```{bash}
ansible-vault edit group_vars/all/vault.yml
```

You can also `ansible-vault decrypt` but need to remember to manually `encrypt`.

These are included in playbooks indirectly. Typically in the appropriate
`group_vars` YAML file, you'll see a stanza such as:
```{yaml}
db_name: {{ vault_db_name }}
```

Sometimes the variable will be common across projects, but will be overriden
in a specific `vault.yml`.

## Adding a playbook

The rough order of creating a playbook is:

  1. Copy over an appropriate playbook as a template that is either production
  or QA. Generally QA should follow a similar project's QA template, staging should
  use production (and broadly those will be the same). Staging requires the
  special roles `prep_staging` and `finalize_staging`.
  2. Create a group in hosts (QA and production
    are or should be separate):
    ```
    [mygroup]
    hostname.of.server.edu
    ```
  4. You will also want to make sure that the group names match and that staging and your project's child files are properly grouped, i.e. all children of staging need to be in
  `[staging:children]` and all children of your project need to be in
  `[project:children]`.
  5. Create a YAML directory in `group_vars` that has a name mirroring the new
  playbook: i.e. if the playbook is `my_playbook_qa`, the name should be
  the same, with a `vars.yml` and a `vault.yml` (for encrypted variables).
  You will also want to create a `group_vars` folder for the project to hold
  variables common to production, qa and staging. It should have the same name
  as the `project:children` you defined earlier in `hosts`.
  6. Reference any playbook variables and set accordingly. See above under
  vault variables for how to configure those.
  6. Add roles to the list in the new playbook in the order needed.
  7. N.B. Make sure you set the `group_name` variable appropriately as some QA
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
