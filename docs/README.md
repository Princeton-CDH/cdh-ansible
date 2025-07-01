# Documentation for CDH ansible playbooks and project infrastructure

## Application-specific documentation

- [Prodigy](applications/prodigy.md)
- [Princeton Geniza Project](applications/geniza.md)

## General

CDH ansibilized applications are deployed to virtual servers managed by PUL.

Typically servers are running Ubuntu Linux, and we have two VMs for each environment (staging and production). For historical reasons and for brevity, our server names use `-test` for staging environments (e.g., for PPA the staging servers are cdh-test-prosody1 and cdh-test-prosody2).

We usually only install one application per VM; the current exception is the sandbox machine, which is set up to allow installation of multiple small, experimental applications.

In a few instances, we are using PUL cloud VMs for more experimental apps that are not production level but which we do not want restricted to campus IPs. This currently only applies to GeoTaste and SimRisk. We're using Google Cloud servers, but AWS is available. PUL typically uses these for short-term experimentation and testing of new applications before configuring and automating deployment on internal VMS.

## Access to PUL VMs (How to Add a New Person to PUL VMs)

### Step 1: Add GitHub account to [princeton_ansible variables](https://github.com/pulibrary/princeton_ansible/blob/main/group_vars/all/vars.yml#L115)

CDH RSE team members access PUL-managed servers using SSH via the `pulsys` (PUL Systems) account.

Access requires SSH keys linked to the team member's GitHub account. These are managed in [princeton_ansible variables](https://github.com/pulibrary/princeton_ansible/blob/main/group_vars/all/vars.yml#L115). Submit a pull request to add an entry under 'cdh_github_keys' (example format: [https://github.com/example_user.keys](https://github.com/example_user.keys)).

To update SSH keys on a specific server (such as a new VM), use the [Update pulsys user keys](https://ansible-tower.princeton.edu/#/templates/job_template/17/details) template in [Ansible Tower](https://ansible-tower.princeton.edu/).

### Step 2: Update SSH key

Check [https://github.com/example_user.keys](https://github.com/example_user.keys) to see available public keys. 

If the page is empty, you need to [generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent). Make sure you complete both steps: "Generating a new SSH key" and "Adding your SSH key to the ssh-agent".

After adding the SSH key, refresh your Github public key page to verify it appears.

### Step 3: Princeton Ansible Tower

1. Navigate to [Princeton Ansible Tower](https://ansible-tower.princeton.edu/#/home)
2. Go to 'templates' on the side bar
3. Find the Job template 'Update pulsys user keys'
4. Click 'launch' to open the dialog box to configure how to run the template
5. In the `limit` field, specify the hostname you need access to (e.g., '[cdh-web3.princeton.edu](http://cdh-web3.princeton.edu/)'). 
    Find hostnames in the [CDH ansible host doc](https://github.com/Princeton-CDH/cdh-ansible/blob/main/inventory/all_hosts). Pay attention to group names (e.g. cdhweb_staging, cdhweb_production), which specify staging vs production servers. Choose the appropriate host based on your environment needs.
6. Keep all other fields at their default values
7. Click 'launch'

This step makes Ansible Tower to deploy your SSH key to the specific server you need access to. 

### Step 4: Verify your access to the CDH server

1. Open your terminal.
2. SSH to the host you just updated access to (e.g., `ssh pulsys@cdh-test-web1.princeton.edu`).
3. Confirm you can successfully log in.
    - If the login works without a password prompt, your key was successfully installed.

Note: The `pulsys` account has full `sudo` permissions. For running applications, we use a non-privileged deploy account called `conan`. To switch to the conan account while logged in as pulsys, simply type `conan` at the command prompt.

### Troubleshooting Tips
- If you're prompted for a password, it usually means your SSH key wasn’t correctly loaded.
- You can run `ssh -v [hostname]` (e.g., `ssh -v pulsys@cdh-test-web1.princeton.edu`) to see what keys your SSH client is trying — look for lines like: `debug1: Offering public key: /Users/you/.ssh/id_ed25519`.
- If no key is offered, your SSH key might not be loaded into your SSH agent. Check by running `ssh-add -l` in the terminal.
    - It should output your SSH key (e.g., `2048 SHA256:xyz... /Users/you/.ssh/id_ed25519 (ED25519)`).
    - If it says `The agent has no identities`, it means your key is not loaded. Load it with `ssh-add ~/.ssh/id_ed25519`.

### (Optional) Automatically load key on login (macOS)
To avoid adding your key manually every time:
- To always use the pulsys account and the appropriate SSH key, add the following snippet to your `~/.ssh/config` (create it if it doesn’t exist: `nano ~/.ssh/config`):
    ```
    Host [hostname] (e.g., cdh-web3.princeton.edu)
        User pulsys
        IdentityFile ~/.ssh/id_ed25519
        IdentitiesOnly yes
    ```






