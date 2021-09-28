Role Name
=========

This role runs setup needed to install and use [browsertrix-crawler](https://github.com/webrecorder/browsertrix-crawler) to create a web archive of a site and push the resulting files to a GitHub repository.

Requirements
------------

The GitHub repository and branch specified in role variables must be created ahead of time.

The public ssh key in `files/github_id.pub` must be added as an allowed key for the user that should be used for pushing the web archive crawl results to GitHub.

Role Variables
--------------

- `browsertrix_crawl_url`: Base url of the site to be crawled and archived
- `browsertrix_crawl_repo`: GitHub repository (in org/name format) where web archive results will go
- `browsertrix_crawl_repo_branch`: branch of the GitHub repository; default is `main`

Dependencies
------------

Depends on the **build_dependencies** role to install the Ubuntu **docker.io** package.

Example Playbook
----------------

The role includes an optional reminder task about next steps that can be run as a post task.

    - hosts: crawl_server
      roles:
        - browsertrix

      post_tasks:
        - name: Reminder about next steps
          include_role:
            name: browsertrix
            tasks_from: start_crawl_reminder
