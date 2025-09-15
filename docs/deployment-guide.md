# **Deployment Guide**

This guide provides instructions for deploying CDH applications using Ansible. It covers:

- Introduction to CDH Deployment environments and default branches
- How to deploy with Ansible Tower using web interface
- How to deploy with local cdh-ansible checkout using command-line

---

## Deployment Environments and Default Branches

CDH applications can be deployed to two environments:

1. **Staging**: Uses `develop` branch by default
2. **Production**: Uses `main` branch by default


---


## Method 1: Deploy with Ansible Tower Web Interface

The simplest way to deploy a CDH application is to use the Ansible Tower web interface. This method offers a graphical interface for running deployments, making it accessible even if you are not familiar with the command line or Ansible itself.

**⚠️ Note:** Not all playbooks are available in Ansible Tower. For playbooks not available in Tower, use the command-line method below.

### Deploy to the Staging Environment

1. Go to [Princeton Ansible Tower](https://ansible-tower.princeton.edu/#/home).
2. Navigate to **Resources** → **Templates** in the sidebar.
3. Search for "CDH" and find the job template for your web app.
4. Click on the **template name** (not the rocket icon) to go to the template's page.
5. On the template page, click the **Launch** button, then:
    1. On the first page ("Credentials") and the second page ("Other prompts"), simply click "Next" without making any changes—use the default settings.
    2. On the third page ("Survey"), select **staging** as the environment. The branch name will default to **develop** (no need to change it unless you are deploying a non-default branch, such as a release or feature branch).
    3. On the fourth page ("Preview"), review your selections and then click **Launch** to start the deployment.

### Deploy to the Production Environment

**⚠️ Note:** We don't deploy to production on Friday afternoons.

1. Follow the same steps as staging deployment above.
2. On the "Survey" page, select **production** as the environment. The branch name will default to **main** (no need to change it unless deploying a non-default branch).

---

## Method 2: Command-Line Deployment

Before you can use the command-line deployment method, you need to have a local copy of the `cdh-ansible` repository on your computer, and then follow [README](../README.md) to set up your local environment before running the deployment.

### Deploy to the Staging Environment

By default, it uses the `develop` branch to deploy to the staging environment.

```bash
ansible-playbook playbooks/your_app.yml
```

### Deploy to the Production Environment

By default, it uses the `main` branch to deploy to the production environment.

```bash
ansible-playbook playbooks/your_app.yml -e runtime_env=production
```

### Deploy a Non-Default Branch

To deploy a specific branch, tag, or commit hash:

**To staging:**
```bash
ansible-playbook playbooks/your_app.yml -e ref=your-branch-name
```

**To production:**
```bash
ansible-playbook playbooks/your_app.yml -e runtime_env=production -e ref=your-branch-name
```

Examples:
```bash
# Deploy release branch to staging
ansible-playbook playbooks/cdhweb.yml -e ref=release/3.15

# Deploy specific tag to production
ansible-playbook playbooks/geniza.yml -e runtime_env=production -e ref=v4.2.1

# Deploy feature branch to staging
ansible-playbook playbooks/prosody.yml -e ref=feature/new-search
```

### Additional Useful Command-Lines

**Increase verbosity:**
```bash
ansible-playbook playbooks/your_app.yml -v
```

**Pause before finalizing deployment:**
```bash
ansible-playbook playbooks/your_app.yml --tags=all,final-pause
```

**Revert a Deployment:**
```bash
ansible-playbook playbooks/revert_deploy.yml -e host_group=your_app_environment
```
