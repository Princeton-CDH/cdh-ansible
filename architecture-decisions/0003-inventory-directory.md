# Use inventory directory for hosts and group variables

* Status: accepted
* Deciders: @rlskoeser, @acozine
* Date: 2024-05-21

## Context and Problem Statement

We want to have the option of running CDH-ansible playbooks on a local development environment or in Ansible Tower. Ansible Tower was unable to  import the CDH inventory from a top-level hosts file (our previous solution); moving the hosts file into an inventory directory allowed Ansible Tower to successfully import the inventory.

However, this change caused problems with group variables. The immediate symptoms made it clear that shared variables in the `all` host group were not getting loaded as expected, causing playbooks to fail almost immediately.

## Decision 

1. We have moved the top-level `hosts` file to `inventory/all_hosts`. For now, we will continue to use a single hosts file.
2. We have moved the `group_vars` directory from the top-level of the repository under `inventory`. This restores the expected behavior of merging variables across host groups (all, staging/production, and specific application groups).

### Consequences 

* This setup should allow us to run playbooks locally or in Ansible Tower
* We can continue to use the single `hosts` file and the `group_vars` structure with variables for multiple host groups.
