Role Name
=========

This role runs setup needed to install and use [browsertrix-crawler](https://github.com/webrecorder/browsertrix-crawler) to create a web archive of a site and push the resulting files to a GitHub repository.

Requirements
------------

The GitHub repository and branch specified in role variables must be created ahead of time.

The public ssh key in `files/github_id.pub` must be added as an allowed key for the user that should be used for pushing the web archive crawl results to GitHub.

Role Variables
--------------

- `browsertrix_crawl_seeds`: List of seed urls to be crawled and archived; must include `url`;  `scopeType` is optional, default scope is `host`
- `browsertrix_crawl_repo`: GitHub repository (in org/name format) where web archive results will go
- `browsertrix_crawl_repo_branch`: branch of the GitHub repository; default is `main`
- `browsertrix_collection`: collection name to be used for the archive (optional)
- `browsertrix_custom_driver`: custom driver to pass to browsertrix for specific interactive behaviors (optional)
- `browsertrix_timeout_seconds`: number of seconds before browsertrix gives up trying to load a URL (optional)


Dependencies
------------

Depends on the **build_dependencies** role to install the Ubuntu **docker.io** package.

Example Playbook
----------------

Example seed variable list:

```yaml
browsertrix_crawl_seeds:
   - url: "https://example.com/"
     scopeType: "host"
   - url: "https://example.com/sitemap.xml"

```

The role includes an optional reminder task about next steps that can be run as a post task.

```yaml
    - hosts: crawl_server
      roles:
        - browsertrix

      post_tasks:
        - name: Reminder about next steps
          include_role:
            name: browsertrix
            tasks_from: start_crawl_reminder
```