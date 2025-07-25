# **Release & Deployment Guide**

## **Quick Overview**

1. **Prep work** – Merge feature branches and verify `develop`/`main` status.
2. **Create a release branch** – Use Git-flow to start and publish the release.
3. **Housekeeping** – Version bump, update changelog, run tests, and fix dependencies.
4. **Deploy to staging** – Use Ansible Tower for acceptance testing.
5. **Acceptance testing** – Notify reviewers and confirm testing passes.
6. **Finish the release** – Merge, tag, and push with Git-flow.
7. **Deploy main to production** – Run Ansible Tower for production.

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
   > **Why?** Git-flow automatically creates `release/3.15` from `develop`. This branch is for final fixes (version bumps, changelog updates, small bug fixes).

4. It's wise to publish the release branch so others can contribute:

   ```bash
   git flow release publish 3.15
   ```



---

## **3. Housekeeping on the Release Branch**

* \[ ] **Version bump**

   Update `__init__.py` and commit the change:

  ```python
  __version_info__ = (3, 15, 0, None)
  ```

* \[ ] **CHANGELOG.rst**

  - Add a new section with the version number and feature list.
  - Check the Iteration Board’s **“Done”** section for completed features.

* \[ ] **DEPLOYNOTES.rst**

    - Document any additional steps needed for deployment (leave empty if none).

* \[ ] **Dependencies**

    - Run `npm audit`, and then `npm audit fix`; commit the updated `package-lock.json`.
    - Run `pip freeze --exclude-editable > requirements.lock`; commit the lockfile.


* \[ ] **Unit Tests & GitHub Actions**

  - Run the test suite (pytest), make sure unit tests are passing.
  - Push the release branch once to trigger GitHub Actions.
  - Fix any failing checks.

---

## **4. Deploy Release Branch to Staging with Ansible**

1. Go to [Princeton Ansible Tower](https://ansible-tower.princeton.edu/#/home).
2. Navigate to **Templates** (sidebar).
3. Search for "CDH" and find the job template for your web app.
4. Click **Launch**, then:

    1. Leave **Source Control Branch**, **Job Tags**, and **Skip Tags** as default.
    2. Choose **staging** as the environment.
    3. Enter your release branch name (e.g., `release/3.15`).
    4. Go to **Next**, preview, and **Launch**.

> **Result:** Your release branch is deployed to staging and ready for acceptance testing.

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

    > Git-flow will:
    >
    > * Merge `release/3.15` into both `main` and `develop`
    > * Tag the release
    > * Delete the release branch (locally)

2. During this process, **Vim will open twice**:

    * **Merge message:** Can just copy-paste from `CHANGELOG`.
    * **Tag message:** Enter `Release 3.15`.

    > Both messages are required: forgetting to add will cause the command to abort

3. Remember to push tags to remote (Git-flow does not do this automatically):

    ```bash
    git push origin main develop
    git push origin --tags
    ```

    > Hint: You can check local tags with `git tag`.

---

## **7. Deploy Main to Production with Ansible**

> **Note:** We don't do deployment Friday afternoon.

1. Go to [Princeton Ansible Tower](https://ansible-tower.princeton.edu/#/home).
2. Navigate to **Templates**.
3. Search "CDH" and find the job template for your web app.
4. Click **Launch**, then:

    1. Leave **Source Control Branch**, **Job Tags**, and **Skip Tags** as default.
    2. Choose **production** as the environment.
    3. Enter `main` in “What branch would you like to deploy?”
    4. Go to **Next**, preview, and **Launch**.

> **Result:** Main is deployed to production. 🎉

* [ ] Remember to announce in the project Slack channel that the new version is live and remind people what changes are available now. If there are many updates, link to the `CHANGELOG`. 

