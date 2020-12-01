Role Name
=========

Create a database and user account on a remote postgres server. Requires `postgres_admin_user` and `postgres_admin_password` to be defined so that the admin user can create the new user and database.

Example Playbook
----------------

```yml
    - hosts: servers
      roles:
         - postgresql
```

License
-------

See [LICENSE](https://github.com/Princeton-CDH/CDH_ansible/blob/main/LICENSE).
