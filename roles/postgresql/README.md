Role Name
=========

Connects to a remote postgres server and uses provided admin credentials to create a new database and user account for a given application.

Based on [the `postgresql` role from `pulibrary/princeton_ansible`](https://github.com/pulibrary/princeton_ansible/tree/main/roles/postgresql).

Variables
---------

- `postgres_port`: port at which remote postgres server is accessible
- `postgres_host`: hostname for remote postgres server
- `postgres_version`: version of postgres in use
- `postgres_admin_user`: account on postgres server with db creation permissions
- `postgres_admin_password`: password for admin postgres account
- `application_db_name`: postgres database to create for app
- `application_dbuser_name`: postgres account for app that will be created with access to app's database 
- `application_dbuser_password`: password for app's postgres account
- `application_dbuser_role_attr_flags`: capabilities to grant to app's postgres account

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
