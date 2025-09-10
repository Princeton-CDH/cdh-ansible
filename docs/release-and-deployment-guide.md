# **Deployment Guide**

## **What This Guide Covers**

This guide provides instructions for deploying CDH applications using Ansible. It covers:

- Deployment environments and default branches for CDH applications
- Deploying with Ansible Tower using web interface
- Command-line deployment from local cdh-ansible checkout
- Deploying non-default branches
- Post-deployment tasks

---

## **Deployment Environments and Default Branches**

CDH applications can be deployed to two environments:

- **Staging**: Uses `develop` branch by default
- **Production**: Uses `main` branch by default

Some applications may use different default branches. Check the application's `group_vars` for specific configurations.

---

## **Method 1: Deploy with Ansible Tower Web Interface**

**⚠️ Note:** Not all playbooks are available in Ansible Tower. For playbooks not available in Tower, use the command-line method below.

### **Deploy to Staging**

1. Go to [Princeton Ansible Tower](https://ansible-tower.princeton.edu/#/home).
2. Navigate to **Resources** → **Templates** in the sidebar.
3. Search for "CDH" and find the job template for your web app.
4. Click on the **template name** (not the rocket icon) to go to the template's page.
5. On the template page, click the **Launch** button, then:
    1. On the first page ("Credentials") and the second page ("Other prompts"), simply click "Next" without making any changes—use the default settings.
    2. On the third page ("Survey"), select **staging** as the environment. The branch name will default to **develop** (no need to change it unless you are deploying a non-default branch, such as a release or feature branch).
    3. On the fourth page ("Preview"), review your selections and then click **Launch** to start the deployment.

### **Deploy to Production**

**⚠️ Note:** We don't deploy to production on Friday afternoons.

1. Follow the same steps as staging deployment above.
2. On the "Survey" page, select **production** as the environment. The branch name will default to **main** (no need to change it unless deploying a non-default branch).

---

## **Method 2: Command-Line Deployment**

### **Prerequisites**

Following [README](../README.md) to set up your local environment.


### **Deploy to Staging (Default Branch)**

```bash
ansible-playbook playbooks/your_app.yml
```

Examples:
```bash
ansible-playbook playbooks/cdhweb.yml
ansible-playbook playbooks/geniza.yml
```

### **Deploy to Production (Default Branch)**

```bash
ansible-playbook playbooks/your_app.yml -e runtime_env=production
```

### **Deploy a Non-Default Branch**

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

### **Additional Command-Line Options**

**Increase verbosity:**
```bash
ansible-playbook playbooks/your_app.yml -v
```

**Skip GitHub deployment notifications:**
```bash
ansible-playbook playbooks/your_app.yml --skip-tags gh_deploy
```

**Pause before finalizing deployment:**
```bash
ansible-playbook playbooks/your_app.yml --tags=all,final-pause
```

**Include setup tasks (for initial provisioning):**
```bash
ansible-playbook playbooks/your_app.yml --tags=all,setup
```

---

## **Post-Deployment Tasks**

### **Check DEPLOYNOTES**

After deployment, check the application's `DEPLOYNOTES.rst` file for any manual steps required on the server.

### **Find Server Hostnames**

Server hostnames are listed in [`inventory/all_hosts`](../inventory/all_hosts). 
Look for:
- **Staging servers**: `app_name_staging` (e.g., `cdhweb_staging`, `geniza_staging`)
- **Production servers**: `app_name_production` (e.g., `cdhweb_production`, `geniza_production`)

Most applications have two VMs per environment mirroring each other for redundancy.

### **SSH Access**

Connect to servers using:
```bash
ssh pulsys@hostname.princeton.edu
```

### **Testing After Staging Deployment**

After deploying to staging, it's important to verify the deployment:

1. **Create testing instructions** in the relevant GitHub issue
2. **Add the `awaiting testing` label** to trigger Slack notifications
3. **In the project Slack channel**, `@mention` the reviewer and link to the issue
4. **Include a testing deadline** to ensure timely feedback
5. **Verify core functionality** works as expected in the staging environment

---

## **Troubleshooting**

### **Revert a Deployment**

To revert to the previous deployment:
```bash
ansible-playbook playbooks/revert_deploy.yml -e host_group=your_app_environment
```

Example:
```bash
ansible-playbook playbooks/revert_deploy.yml -e host_group=cdhweb_staging
```

### **Common Issues**

- **Vault access errors**: Ensure you're logged into LastPass and the vault identity environment variable is set
- **GitHub token errors**: Set your personal access token or use the fallback token
- **Permission errors**: Ensure you have access to the target servers and vault passwords

---

## **Available Playbooks**

Current playbooks in the repository:
- `cdhweb.yml` - CDH Website
- `derrida_archive.yml` - Derrida Archive
- `derrida_crawl.yml` - Derrida Crawl
- `escriptorium.yml` - eScriptorium (HTR)
- `geniza.yml` - Princeton Geniza Project
- `geotaste.yml` - GeoTaste (sandbox)
- `prodigy.yml` - Prodigy
- `prosody.yml` - Prosody
- `shxco.yml` - Shakespeare and Company Project
- `shxco_datasets.yml` - Shakespeare and Company Datasets
- `simulatingrisk.yml` - Simulating Risk (sandbox)
- `replicate.yml` - Data replication (production to staging)
- `revert_deploy.yml` - Deployment rollback
- `db_setup.yml` - Database setup

**Note:** Not all playbooks may be available in Ansible Tower. Use command-line deployment for playbooks not yet available in Tower.

---

## **Post-Deployment Communication**

After a successful production deployment:

1. **Announce in the project Slack channel** that the new version is live
2. **Summarize key changes** that are now available to users
3. **Link to the CHANGELOG** if there are many updates
4. **Tag relevant team members** who should be aware of the changes

Example announcement:
> 🚀 **Geniza v4.2.1 is now live in production!** 
> 
> Key changes:
> - New advanced search filters
> - Performance improvements for large result sets
> - Bug fixes for transcription display
> 
> Full details: [CHANGELOG.rst](link-to-changelog) 

