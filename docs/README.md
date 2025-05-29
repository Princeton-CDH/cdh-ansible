# Documentation for CDH ansible playbooks and project infrastructure

## Application-specific documentation

- [Prodigy](applications/prodigy.md)
- [Princeton Geniza Project](applications/geniza.md)

## General

CDH ansibilized applications are deployed to virtual servers managed by PUL.

Typically servers are running Ubuntu Linux, and we have two VMs for each environment (staging and production). For historical reasons and for brevity, our server names use `-test` for staging environments (e.g., for PPA the staging servers are cdh-test-prosody1 and cdh-test-prosody2).

We usually only install one application per VM; the current exception is the sandbox machine, which is set up to allow installation of multiple small, experimental applications.

In a few instances, we are using PUL cloud VMs for more experimental apps that are not production level but which we do not want restricted to campus IPs. This currently only applies to GeoTaste and SimRisk. We're using Google Cloud servers, but AWS is available. PUL typically uses these for short-term experimentation and testing of new applications before configuring and automating deployment on internal VMS.

### Access to PUL VMs

CDH RSE team members have access PUL-managed servers using ssh and the `pulsys` (PUL Systems) account.
Access is based on ssh keys associated with team member GitHub accounts; this is managed
in [princeton_ansible variables](https://github.com/pulibrary/princeton_ansible/blob/main/group_vars/all/vars.yml#L115), and we can make request changes via pull requests. If you need to update ssh keys on a particular server (e.g., a newly provisioned VM), use the
[Update pulsys user keys](https://ansible-tower.princeton.edu/#/templates/job_template/17/details) template in [Ansible Tower](https://ansible-tower.princeton.edu). When you launch the job, use the `limit` input to specify the hostnames for the servers you want to update so that it does not have to run on all PUL VMs.

The `pulsys` account has `sudo all` permission. We also have a non-privileged deploy account `conan` (the deployer) which is used for actually running applications.
