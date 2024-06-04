# Set cdh-info GitHub deploy token as default 

* Status: accepted
* Deciders: @rlskoeser, @acozine, @kayiwa, @carolyncole
* Date: 2024-06-04

## Context and Problem Statement

CDH playbooks use the GitHub deployment API to document what version of a codebase (i.e., commit hash, tag, branch) is deployed to which environment (e.g., staging or production). Using this API requires a GitHub credential, which we previously set as an environment variable or a command-line override.  To run these playbooks in Ansible Tower, we need a way to set that GitHub credential as an ansible variable. Tower supports GitHub personal access tokens, but only for webhooks triggered by Tower.

## Decision 

1. A GitHub token for the cdh-info/princetoncdh account with repository deployment permissions has been added to vaulted group variables available to all playbooks/hosts (`all/vault.yml`) and set as the default option for the `github_token` variable in `all/vars.yml`.
2. If the `ANSIBLE_GITHUB_TOKEN` environment variable is set, it will override the vaulted github token (previous behavior).

### Consequences 

* This setup should allow us to run playbooks locally or in Ansible Tower
* Deployment API calls will work whether or not someone has configured an environment variable with a personal access token tied to their account.
* Local deploys will show up as run by the cdh-info/princetoncdh account if a personal token is not used.
