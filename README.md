# CDH Ansible Repository

[![Molecule Tests](https://github.com/Princeton-CDH/cdh-ansible/actions/workflows/molecule_tests.yml/badge.svg)](https://github.com/Princeton-CDH/cdh-ansible/actions/workflows/molecule_tests.yml)

## Overall structure

The overall structure of this repository can be broken down as follows:
  - `playbooks` - collections of roles executed in series against a host.
  - `roles` - the various tasks that Ansible can perform in a group.
  - `inventory` - hosts and variables
    - `all_hosts` - host file with hostnames and host groups 
    - `group_vars` - group variables for different hosts and host groups
      - `all` - variables shared by all playbooks
      - `vars.yml`- unencrypted all variables
      - `vault.yml` - `ansible vault` encrypted variables
  - `architecture-decisions` - list of significant architectural decisions, as markdown files

## Using these playbooks

### Requirements
  - Python virtual environment.
    - See `.python-version` for the recommended version of Python; we recommend [pyenv](https://github.com/pyenv/pyenv) for managing python versions.
    - If you use `env` or `venv`, the `.gitignore` will exclude it.
    - Install python dependencies: `pip install -r requirements.txt`

  -  Install required Ansible galaxy collections and roles:
      - `ansible-galaxy install -r requirements.yml`

  - The CDH Ansible vault keys are stored in LastPass. You need to be added to the appropriate LastPass share and install [lastpass-cli](https://github.com/lastpass/lastpass-cli).  There are two command-line scripts in the `bin/` directory to call `lpass` to retrieve the vault keys, and the default configuration is set in `ansible.cfg`. See below for more details on the vault setup.
  - A GitHub [personal access token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) for any playbook that uses the `create_deployment` and `close_deployment` tasks. You can set this as an environment variable
  as `ANSIBLE_GITHUB_TOKEN` or pass it on the command line as `-e github_token=`


### Precommit hook

If you plan to contribute to this repository, you should install the configured pre-commit hooks. (If you installed python dependencies, pre-commit should already be installed)

```{bash}
pre-commit install
```

This will add install a pre-commit hook to prevent committing an unencrypted vault or private key file. If new encrypted files are added with different names, filename patterns should be added to the pre-commit configuration in `.pre-commit-config.yaml`

> **_NOTE:_**  If you have a previous installation with the local pre-commit hook script that was included in this repository, you will need to run `pre-commit install -f` to replace it.

## Running a playbook

To run a playbook, with your python virtual environment activated:

```{bash}
ansible-playbook playbooks/name_of_playbook.yml
```

Each application has a deploy playbook that can be used to deploy that application to either the production or staging environments. By default, the playbook will deploy to staging. To deploy to production, override the runtime environment with this command line option: `-e runtime_env=production`

By default, deploying to production will deploy the `main` branch of the github repository for that application; deploying to staging will deploy the `develop` branch. These may be overridden by specific applications with different conventions.

To deploy a branch or tag other than the default, you can specify an alternate git reference via `-e ref=GITREF` where `GITREF` is the name of the branch, tag, or a commit hash.

The playbook will run, noting success and failures. The `-v` flag adjusts verbosity (adding more `v`s will produce more verbosity. Debug tasks are usually written at `2`)

### Skip setup tasks

By default, initial provisioning and setup tasks are configured to be skipped.  Tasks or groups of tasks should be tagged with both `setup` and `never`.

To run playbook without skipping setup tasks, pass the `setup` and `all` tags, so untagged tasks and tasks tagged `setup` run:

```{bash}
ansible-playbook --tags=all,setup playbooks/name_of_playbook.yml
```

### Skip deployment tasks

By default, most playbooks create a [GitHub deployment](https://docs.github.com/en/rest/deployments/deployments?apiVersion=2022-11-28), which is used to track which version of the code is deployed to which environment. Through Slack/GitHub integration, GitHub deployments can be used to notify team members when a deploy is taking place and whether or not it succeeds or fails.  (This can be very noisy when working on or troubleshooting a deploy.)

The tasks for creating and closing the GitHub deployment are tagged with `gh_deploy`. If you want to run a playbook without deploying code, pass `--skip-tags gh_deploy`.

## Pause before finalizing deploy

If you want to pause the playbook before the new version is switched live,
there is an optional pause step you can enable using tags. When running normally and skipping setup tasks, run as follows:

```{bash}
ansible-playbook --tags=all,final-pause playbooks/playbook.yml
```

When running with setup steps enabled:

```{bash}
ansible-playbook --tags=all,setup,final-pause playbooks/playbook.yml
```

## Revert last deploy

To revert to previous deploy run call the `revert_deploy` playbook with a `host_group` matching the deploy you want to revert, e.g.:

```{bash}
ansible-playbook -e host_group=shxco_staging playbooks/revert_deploy.yml
```

## Vault variables and passwords

Variables kept in `inventory/group_vars/*/vault.yml` are sensitive configurations
that should always be kept encrypted on commit. To edit them (in your system text editor):
```{bash}
ansible-vault edit inventory/group_vars/all/vault.yml
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
contractor access for running geniza and geniza_staging playbooks without full access
to all credentials.  For compatibility with Ansible Tower, these are no longer
defined in the default ansible.cfg but shell scripts are provided to
pull the appropriate password from LastPass. For the default configuration,
set the following environment variables:
```sh
ANSIBLE_VAULT_IDENTITY_LIST=default@bin/lpass_default.sh,geniza@bin/lpass_geniza.sh
```

Because there are multiple vault ids, encrypting requires specifying which
vault id to use. Geniza variables and setup files should be encrypted with
`--encrypt-vault-id geniza` ; all other vaulted files should be encrypted with
the default vault password.


These are included in playbooks indirectly. Typically in the appropriate `group_vars` YAML file, you'll see a stanza such as:
```{yaml}
db_name: {{ vault_db_name }}
```

Some encrypted variables are shared across projects and playbooks. Shared variables may be
overriden in a project- or playbook-specific `vault.yml` file.

## Replication

Copying production data from production to staging can be done for some projects
using a special replication playbook. It is defined with multiple hosts, but
for typical use you should limit to the host group you want to replicate, e.g.:

```{bash}
ansible-playbook playbooks/replicate.yml --limit=geniza
```

On subsequent runs for the same host group on the same day, to skip regenerating
production database dumps and media archive files, you can limit to just the staging host:

```{bash}
ansible-playbook playbooks/replicate.yml --limit=geniza_staging
```

Currently replication consists of:
- dumping the production database, restoring it to staging, and running
  django migrations in the current deploy
- update django sites in the database to match the staging environment
- backing up and restoring any user-uploaded media files and setting correct ownership and permissions

Replication does not yet include restoring Solr indexing or support replication to dev environments.

### Setting up replication for a new project

- Add the appropriate production and staging host names to the source and destination plays
- Define a new variable `replication_source_host` in the staging variables; it should reference the corresponding ansible hostname (e.g., for geniza `replication_source_host` is set to `geniza_production`)
- If database names differ between staging and production, you may need to override the `db_backup_filename` for the staging host variables.
- Ensure that the staging host has an `application_url` variable defined; this is needed to correctly set the Django site entry in the migrated database.


## Adding a playbook

Recommended steps for adding a new playbook:

  1. Copy over an appropriate playbook for a similar application to use as a starting point, and modify the list of roles as needed.
  2. Define separate staging and production host groups for the application.
  3. Add the staging host group to the staging group by including them in the list of `[staging:children]`, and create an application group that collects both staging and production host groups.
  5. Add new `group_vars` directories as needed to configure the application or override any defaults.  Variables that are relevant for all environments should be set as application group variables; environment-specific configurations can be set in `_staging` or `_production` group variables.

## Documenting architectural decisions

We use the [ADR specification](https://github.com/joelparkerhenderson/architecture_decision_record) for documenting architectural decisions made over the course of work on this repository - i.e. conventions around our usage of Ansible. Decision documents are stored in the `architecture-decisions/` folder as markdown files.

To propose or doucment a new decision, copy the `architecture-decisions/template.md` file and rename it using a sequential number and description of the decision that needs making. Decisions that require discussion should be proposed using a pull request for discussion and review.

## To run the geniza deploy only

- Ensure you have access to the geniza ansible vault key in LastPass
- Install lastpass cli
- Set the following environment variables:
```sh
ANSIBLE_VAULT_IDENTITY_LIST=geniza@bin/lpass_geniza.sh
GENIZA_DEPLOY_ONLY=1
```

Note that you will not be able to run setup tasks or decrypt setup vault secrets.
