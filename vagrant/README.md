# Staging Vagrant

## Running the staging vagrant VM

From this directory, after you have installed Vagrant and VirtualBox for your
OS (MacOS or Linux for this build), run `vagrant up`. The provision and building
will take a considerable amount of time.

## Running a staging playbook

With the provisioned and running VM, from the top level directory, and
any Ansible password files appropriately in your environment (via
`ANSIBLE_VAULT_PASSWORD_FILE` pointing to the key), run:

```{bash}
ansible-playbook project_staging.yml
```

If everything is working correctly, the playbook will deploy and a Django
application will be open on `localhost:8080`. Since Princeton CAS will not work
readily in the VM, an admin user with the (not at all) secure username `admin`
and password `adminpass` will be available to you for your use.

## Running npm or python for the project

The project uses python loaded using the SCL (Software Collection Library).
These modules provide up to date system packages for programming languages that
move much more quickly than enterprise cycles.

You'll want to work on the project folder as `deploy`, (easiest way to become deploy
as `vagrant` is `sudo su - deploy`).

To list installed SCLs:

```{bash}
scl --list
```

To load one into your bash shell:

```{bash}
scl enable rh-python35 bash
```

You can repeat this as necessary (if say you need `rh-nodejs6`).
The project group level of Ansible variables
will generally tell you what modules that project uses based on the paths loaded.

Once you have an approriate python, from the appropriate folder, i.e.
`/srv/www/prod/current`, run `source env/bin/activate` to load the project
virtual environment.

## What this setup does not handle

There is one area that this setup does not handle: Solr. The provisioning does
install a Solr in its default configuration (not quite where Springdale puts it
but close enough for testing work). It is up to you to create cores and run
any `manage.py` commands to make it work.

### Create a Solr core
From the `vagrant` folder, `vagrant ssh` and then `sudo su - solr` to become `solr`

To create a core with basic_configs:

```{bash}
/opt/solr/bin/solr create -c myCore -n basic_configs
```

### Where are Solr configs

Configs and data live in `/var/solr/`.
