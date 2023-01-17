# CDH Ansible Repository

[![Molecule Tests](https://github.com/Princeton-CDH/cdh-ansible/actions/workflows/molecule_tests.yml/badge.svg)](https://github.com/Princeton-CDH/cdh-ansible/actions/workflows/molecule_tests.yml)

## Overall structure

The overall structure of this repository can be broken down as follows:
  - `playbooks` - collections of roles executed in series against a host.
  - `roles` - the various tasks that Ansible can perform in a group.
  - `group_vars` - the group variables for different deploys
    - `all` - any variables shared by all deploys
      - `vars.yml`- unencrypted all variables
      - `vault.yml` - `ansible vault` encrypted variables
    - Individual project group variables
  - `hosts` - host file with groups and their associated host(s)
  - `adr` - list of significant architectural decisions, as markdown files

## Using these playbooks

### Requirements
  - Python virtual environment.
    - See `.python-version` for the recommended version of Python.
    - If you use `env` or `venv`, the `.gitignore` will exclude it.

  -  Install required Ansible galaxy collections:
      - `ansible-galaxy install -r requirements.yml`

  - The CDH Ansible vault key. This can be referenced on the command line, but it is
  recommende to set it as an environment variable; e.g., for BASH
   `export ANSIBLE_VAULT_PASSWORD_FILE=/path/to/.passwd`
  - A GitHub [personal access token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) for any playbook that uses the `create_deployment` and `close_deployment` tasks. You can set this as an environment variable
  as `ANSIBLE_GITHUB_TOKEN` or pass it on the command line as `-e github_token=`
  - The CDH deploy bot key. This can be added to ssh-agent or in `~/.ssh/config`. All production deploys must be on the campus network (including VPN) and proxy through the QA server to production, with an ssh config stanza that looks something like:
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

If you plan to contribute to this repository, you should install the configured pre-commit hooks:

```{bash}
pre-commit install
```

This will add install a pre-commit hook to prevent committing an unencrypted vault or private key file. If new encrypted files are added with different names, filename patterns should be added to the pre-commit configuration in `.pre-commit-config.yaml`

> **_NOTE:_**  If you have a previous installation with the local pre-commit hook script that was included in this repository, you will need to run `pre-commit install -f` to replace it.

## Running a playbook

To run a playbook, from your virtual environment, simply invoke:

```{bash}
ansible-playbook playbooks/name_of_playbook.yml
```

QA playbooks should point by default to the develop branch and production playbooks (denoted by an absence of `_qa` suffix) to main.

To deploy a different reference (hash, tag, or branch), use the syntax:

```{bash}
ansible-playbook -e ref=GITREF playbooks/name_of_playbook.yml
```

The playbook will run, noting success and failures. The `-v` flag adjusts verbosity (adding more `v`s will produce more verbosity. Debug tasks are usually written at `2`)

### Skip setup tasks

By default, initial provisioning and setup tasks are configured to be skipped.  Tasks or groups of tasks should be tagged as `setup`.

To run playbook without skipping setup tasks, override the default skip tag configuration:

```{bash}
env ANSIBLE_SKIP_TAGS= ansible-playbook playbooks/name_of_playbook.yml
```

Note that `--skip-tags=[]` doesn't work because the skip tags setting in
`ansible.cfg` takes precedence over command line options.

## Revert last deploy

To revert to previous deploy run call the `revert_deploy` playbook with a `host_group` matching the deploy you want to revert, e.g.:

```{bash}
ansible-playbook -e host_group=shxco_qa playbooks/revert_deploy.yml
```

## Vault variables and passwords

Variables kept in `group_vars/*/vault.yml` are sensitive configurations
that should always be kept encrypted on commit. To edit them (in your system text editor):
```{bash}
ansible-vault edit group_vars/all/vault.yml
```

You can also `ansible-vault decrypt` but need to remember to `encrypt`
after editing. (Pre-commit check will flag if you fail to do so.)


Ansible vault passwords are stored in shared LastPass vault and loaded
using [lastpass-cli](https://lastpass.github.io/lastpass-cli/lpass.1.html).

```{bash}
brew install lastpass-cli
lpass login <email@email.com>
```

There are two different vault passwords (default and geniza), to allow limited
contractor access for running geniza and geniza_qa playbooks without full access
to all credentials. Both are defined in the default ansible.cfg file
with shell scripts to pull the appropriate password from LastPass. To set a single
vault, you can override the config setting with the **ANSIBLE_VAULT_IDENTITY_LIST**
environment variable.

Because there are multiple vault ids, encrypting requires specifying which
vault id to use. Geniza variables and setup files should be encrypted with
`--encrypt-vault-id geniza` ; all other vaulted files should be encrypted with
the default vault password.


These are included in playbooks indirectly. Typically in the appropriate `group_vars` YAML file, you'll see a stanza such as:
```{yaml}
db_name: {{ vault_db_name }}
```

Some encrypted variable ase used across playbooks, but may be
overriden in a project or playbook specific `vault.yml` file.

## Replication

Copying production data from production to qa can be done for some projects
using a special replication playbook. It is defined with multiple hosts, but
for typical use you should limit to the host group you want to replicate, e.g.:

```{bash}
ansible-playbook playbooks/replicate.yml --limit=geniza
```

Currently replication consists of:
- dumping the production database, restoring it to qa, and running any django migrations
- update django sites in the database to match the qa environment
- backing up and restoring any user-uploaded media files and setting correct ownership and permissions

Replication does not yet include restoring Solr indexing or support replication to dev environments. 

### Setting up replication for a new project

- Add the appropriate production and qa host names to the source and destination plays
- Define a new variable `replication_source_host` in the qa variables; it should reference the corresponding ansible hostname (e.g., for geniza `replication_source_host` is set to `geniza_prod`)
- If database names differ between qa and production, you may need to override the `db_backup_filename` for the qa host variables.


## Adding a playbook

The rough order of creating a playbook is:

  1. Copy over an appropriate playbook as a template that is either production or QA.
  2. Create a group in hosts (QA and production are or should be separate):
    ```
    [mygroup]
    hostname.of.server.edu
    ```
  4. You will also want to make sure that the group names match and that your project's child files are properly grouped, i.e. all children of qa need to be in `[qa:children]` and all children of your project need to be in `[project:children]`.
  5. Create a YAML directory in `group_vars` that has a name mirroring the new playbook: i.e. if the playbook is `my_playbook_qa`, the name should be the same, with a `vars.yml` and a `vault.yml` (for encrypted variables). You will also want to create a `group_vars` folder for the project to hold variables common to production, qa and staging. It should have the same name as the `project:children` you defined earlier in `hosts`.
  6. Reference any playbook variables and set accordingly. See above under vault variables for how to configure those.
  6. Add roles to the list in the new playbook in the order needed.

## Documenting architectural decisions

We use the [ADR specification](https://github.com/joelparkerhenderson/architecture_decision_record) for documenting architectural decisions made over the course of work on this repository - i.e. conventions around our usage of Ansible. Decision documents are stored in the `adr/` folder as markdown files.

To propose a new decision, copy the `adr/template.md` file and rename it using a sequential number and description of the decision that needs making. Then create a pull request to track discussion on that decision.


## To run the geniza deploy only

- Ensure you have access to the geniza ansible vault key in LastPass
- Install lastpass cli
- Set the following environment variables:
```sh
ANSIBLE_VAULT_IDENTITY_LIST=geniza@bin/lpass_geniza.sh
GENIZA_DEPLOY_ONLY=1
```

Note that you will not be able to run setup tasks or decrypt setup vault secrets.

