Role Name
=========

Creates a user account on the target system for running deployed applications. Also creates a group with the same name as the user, and ensures that the user is a member of both the new group and the webserver group so that it can write to logfiles.

Variables
---------

- `deploy_user`: name for the new user account and its new group
- `deploy_user_shell`: path to shell to use for the new user
- `webapp_group`: name of web app webserver group on target system (default: www-data)

Example Playbook
----------------

```yml
    - hosts: servers
      roles:
         - deploy_user
```

License
-------

See [LICENSE](https://github.com/Princeton-CDH/CDH_ansible/blob/main/LICENSE).