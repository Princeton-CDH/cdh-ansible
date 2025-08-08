# **Release & Deployment Guide**

## **What This Guide Covers**

This guide is designed as a complete reference for developers who need to release and deploy applications using the CDH Ansible infrastructure. It combines:

- **General CDH release workflow** (steps 1-3, 5-6): Git-flow branching, version bumps, changelog updates, and testing procedures that apply to most CDH software projects
- **Ansible-specific deployment steps** (steps 4, 7): Using Princeton Ansible Tower to deploy applications to staging and production environments

---

## **1. Prep Work**

* [ ] Open a new issue using the **`Software release checklist`** template. Title it with version number (e.g. “Software release checklist for v3.15.”)
* [ ] Confirm all required **feature branches are merged into `develop`**.
* [ ] Pull the latest code and verify `develop` and `main` are up to date.

---

## **2. Create the Release Branch with Git-flow**

1. Switch to the `develop` branch.
2. Initialize Git-flow (if not already set up):
   
   ```bash
   git flow init
   ```
3. Start the release branch (replace `3.15` with your version):

   ```bash
   git flow release start 3.15
   ```
   
   **Why?** Git-flow automatically creates `release/3.15` from `develop`. This branch is for final fixes (version bumps, changelog updates, small bug fixes).

4. It's wise to publish the release branch so others can contribute:

   ```bash
   git flow release publish 3.15
   ```



---

## **3. Housekeeping on the Release Branch**

**💡 Tip:** Consider creating a pull request for the release branch to provide visibility into any code changes made during the release process. This is especially helpful for tracking version bumps, dependency updates, and other release-specific modifications.

* \[ ] **CHANGELOG.rst**

  - Review the changelog to ensure all features and changes are documented.
  - Verify that the changelog is up-to-date with changes merged into `develop`.
  - Add the release version number and date if not already present.

* \[ ] **DEPLOYNOTES.rst**

    - Document any additional steps needed for deployment (leave empty if none).

* \[ ] **Dependencies**

    - **If the project includes JavaScript/Node.js:** Run `npm audit`, and then `npm audit fix`; commit the updated `package-lock.json`.
    - **If the project includes Python:** Run `pip freeze --exclude-editable > requirements.lock`; commit the lockfile.


* \[ ] **Unit Tests & GitHub Actions**

  - **If the project includes Python:** Run the test suite (pytest), make sure unit tests are passing.
  - Push the release branch once to trigger GitHub Actions.
  - Fix any failing checks.

---

## **4. Deploy Release Branch to Staging with Ansible**

1. Go to [Princeton Ansible Tower](https://ansible-tower.princeton.edu/#/home).
2. Navigate to **Resources** → **Templates** in the sidebar.
3. Search for "CDH" and find the job template for your web app.
4. Click on the **template name** (not the rocket icon) to go to the template's page.
5. On the template page, click the **Launch** button, then:

    1. On the first page ("Credentials") and the second page ("Other prompts"), simply click "Next" without making any changes—use the default settings.
    2. On the third page ("Survey"), select **staging** as the environment, and enter your release branch name (for example, `release/3.15`).
    3. On the fourth page ("Preview"), review your selections and then click **Launch** to start the deployment.

5. Check `DEPLOYNOTES` to see if there's any commands you need to manually run on server.

    - Find server hostnames in the [`all_hosts`](../inventory/all_hosts) inventory file. Look for **staging** group names (e.g., `cdhweb_staging`, `geniza_staging`, `prosody_staging`) to identify the correct staging servers.

**✅ Result:** Your release branch is deployed to staging and ready for acceptance testing.


---

## **5. Acceptance Testing**

1. In the issue, add a **Testing Instructions** section as checkboxes (what to test, pass criteria, etc.).
2. Add the **`awaiting testing`** label to relevant GitHub issues (triggers Slack notification).
3. In the project **Slack channel** (not DM), `@mention` the reviewer and link to the issues.
  Include a testing deadline.
4. Wait for testing confirmation. If passed, proceed.

---

## **6. Finish the Release with Git-flow**

1. Finish the release:

    ```bash
    git flow release finish 3.15
    ```

    Git-flow will:
    
    * Merge `release/3.15` into both `main` and `develop`
    * Tag the release
    * Delete the release branch (locally)

2. During this process, **your configured Git editor will open twice**:

    * **Merge message:** Can just copy-paste from `CHANGELOG`.
    * **Tag message:** Enter `Release 3.15`.

    **Important:** Both messages are required: forgetting to add will cause the command to abort

3. Remember to push tags to remote (Git-flow does not do this automatically):

    ```bash
    git push origin main develop
    git push origin --tags
    ```

    **Hint:** You can check local tags with `git tag`.

4. Verify the release tag appears on GitHub by checking the repository's tags/releases page to confirm the push was successful.

---

## **7. Deploy Main to Production with Ansible**

**⚠️ Note:** We don't do deployment Friday afternoon.

1. Go to [Princeton Ansible Tower](https://ansible-tower.princeton.edu/#/home).
2. Navigate to **Resources** → **Templates** in the sidebar.
3. Search "CDH" and find the job template for your web app.
4. Click on the **template name** (not the rocket icon) to go to the template's page.
5. On the template page, click the **Launch** button, then:

    1. On the first page ("Credentials") and the second page ("Other prompts"), simply click "Next" without making any changes—use the default settings.
    2. On the third page ("Survey"), select **production** as the environment, and enter **main** as the release branch name.
    3. On the fourth page ("Preview"), review your selections and then click **Launch** to start the deployment.

5. Check `DEPLOYNOTES` to see if there's any commands you need to manually run on server.

    - Find server hostnames in the [`all_hosts`](../inventory/all_hosts) inventory file. Look for **production** group names (e.g., `cdhweb_production`, `geniza_production`, `prosody_production`) to identify the correct production servers.


**🎉 Result:** Main is deployed to production!

**📢 Remember:** Announce in the project Slack channel that the new version is live and remind people what changes are available now. If there are many updates, link to the `CHANGELOG`. 

