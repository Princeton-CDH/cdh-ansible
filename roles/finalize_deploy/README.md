finalize_deploy
===============

This role runs all of the tasks needed to make the new code live, with a handler to restart apache and clean up old deployments.

It assumes the standard configuration /srv/www symlinks to /var/www used in CDH Django projects.

Variables
---------

- `deploy`: path to the new deployment directory
- `install_root`: root directory where deployments are stored (e.g., /srv/www/geniza)
- `symlink`: name of the symlink in /var/www/
- `deploy_user`: user account for running deployed applications
- `auto_cleanup_deploys`: whether to automatically clean up old deployments (default: true)
- `deploy_keep_count`: number of recent deployments to keep when cleaning up (default: 3)

Example Playbook
----------------

```yml
- hosts: servers
  roles:
     - finalize_deploy
  vars:
    deploy: "/srv/www/myapp/4.1.0-abc123"
    install_root: "/srv/www/myapp"
    symlink: "myapp"
    auto_cleanup_deploys: true
```

License
-------

See [LICENSE](https://github.com/Princeton-CDH/CDH_ansible/blob/main/LICENSE).