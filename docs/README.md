# Documentation for CDH ansible playbooks and project infrastructure

## Application-specific documentation

- [Prodigy](applications/prodigy.md)

## General

CDH ansibilized applications are deployed to virtual servers managed by PUL.

Typically servers are running Ubuntu Linux, and we have two VMs for each environment (staging and production). For historical reasons and for brevity, our server names use `-test` for staging environments (e.g., for PPA the staging servers are cdh-test-prosody1 and cdh-test-prosody2).

We access PUL-managed servers using ssh and the `pulsys` (PUL Systems) account.
Access is based on ssh keys associated with team member GitHub accounts; this is managed
in [princeton_ansible variables](https://github.com/pulibrary/princeton_ansible/blob/main/group_vars/all/vars.yml#L115). If you need to update ssh keys on a particular server, you can use the
"Update pulsys user keys" template in Ansible Tower and limit to the appropriate servers.

The `pulsys` account has `sudo all` permission. We also have a non-privileged deploy account (`conan` the deployer) which is used for actually running applications.
