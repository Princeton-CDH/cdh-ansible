# eScriptorium / htr2hpc

[eScriptorium](https://gitlab.com/scripta/escriptorium) is an open-source handwritten text recognition (HTR) application. CDH runs a customized instance that integrates with Princeton's HPC clusters via the [htr2hpc](https://github.com/Princeton-CDH/htr2hpc) package.

- eScriptorium software: https://gitlab.com/scripta/escriptorium
- htr2hpc software: https://github.com/Princeton-CDH/htr2hpc

## Deploying

The eScriptorium application, including the htr2hpc package, is deployed to
staging or production with the `escriptorium` playbook. Staging is the default;
pass `-e runtime_env=production` for production.

Two variables control what gets deployed:

- `ref`: the eScriptorium git ref (tag or branch)
- `htr2hpc_gitref`: the htr2hpc git ref (branch or release tag). Defaults to
  `develop` on staging and `main` on production.

Example staging deploy:

```sh
ansible-playbook playbooks/escriptorium.yml -e ref=v1.0.1 -e htr2hpc_gitref=develop --skip-tags db_backup
```

To deploy a new htr2hpc release to production, set `htr2hpc_gitref` to the
release tag (release tags have no `v` prefix):

```sh
ansible-playbook playbooks/escriptorium.yml -e runtime_env=production -e htr2hpc_gitref=0.9.0
```

## Updating htr2hpc

There is no separate step for updating htr2hpc: every run of the playbook
reinstalls the htr2hpc package from `htr2hpc_gitref`, even if the version string
has not changed (pip is run with `--force-reinstall --no-deps`, because pip
compares version strings, not commit SHAs). To pick up new commits on a branch,
or to deploy a new release, run the playbook again.

- `--no-deps` means new htr2hpc dependencies are **not** installed automatically;
  add them to the playbook configuration before deploying a release that needs them.
- On staging, the exact htr2hpc commit that was installed is written to the
  eScriptorium local settings as `HTR2HPC_GITREF`. Production leaves it unset, so
  htr2hpc uses its own release tag.
- Celery, nginx, and Django Channels are restarted to pick up the new code.

## Wagtail content management

CDH's instance uses htr2hpc's optional Wagtail content management features.
The `python_extra_packages` setting in `inventory/group_vars/htr/vars.yml`
installs htr2hpc with the `all` optional dependency group (`htr2hpc[all]`),
which includes Wagtail, so no extra step is needed to install it.

## First deploy of a new instance

After deploying a new instance for the first time, load the content fixture to
pre-populate the Wagtail admin with the default page snippets (the homepage
heading and the profile page HPC instructions):

```sh
manage.py loaddata cdh_snippets
```

For other initial setup after a new deployment, see
[Configure Site domain](https://github.com/Princeton-CDH/htr2hpc/blob/main/README.md#configure-site-domain)
in the htr2hpc README.
