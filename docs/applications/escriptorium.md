# eScriptorium / htr2hpc

[eScriptorium](https://gitlab.com/scripta/escriptorium) is an open-source handwritten text recognition (HTR) application. CDH runs a customized instance that integrates with Princeton's HPC clusters via the [htr2hpc](https://github.com/Princeton-CDH/htr2hpc) package.

- eScriptorium software: https://gitlab.com/scripta/escriptorium
- htr2hpc software: https://github.com/Princeton-CDH/htr2hpc

## Related playbooks

- The eScriptorium application can be deployed to staging or production with
  the `escriptorium` playbook. Staging is the default; pass `-e runtime_env=production`
  for production.
- To update only the htr2hpc package without a full redeploy, use the
  `reinstall-htr2hpc` tag (see below).

## Updating htr2hpc

The full deploy playbook does **not** reinstall the htr2hpc Python package by
default — it only runs when eScriptorium itself is being redeployed. To update
htr2hpc to a new release, use the `reinstall-htr2hpc` tag:

```sh
ansible-playbook playbooks/escriptorium.yml -t reinstall-htr2hpc
```

This tag uninstalls the current htr2hpc package and reinstalls the version
specified by `htr2hpc_gitref` (defaults to `main`). To deploy a specific
branch or tag, override the variable:

```sh
ansible-playbook playbooks/escriptorium.yml -t reinstall-htr2hpc -e htr2hpc_gitref=0.6.0
```

After reinstalling, the task restarts nginx, Celery, and Django Channels to
pick up the new code. Use this tag whenever a new htr2hpc release has been
published and needs to be deployed — it is not needed for other playbook changes.
