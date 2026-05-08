# prodigy_setup

Deploy and configure an instance of Prodigy for CDH projects.

This role prepares the Prodigy install directory, creates the expected
Muse recipe and data directories, downloads Prodigy recipe files, copies
task data and instruction files from TigerData, writes the Prodigy
configuration file, and installs an nginx site configuration that proxies
traffic to Prodigy on port `8080`.

## Requirements

This role currently targets Ubuntu Jammy.

The target host is expected to have access to the source files referenced
by:

- `prodigy_datafile_src`
- `prodigy_instruct_src`

For production use, these files commonly live on TigerData.

The role also expects nginx to be installed when nginx configuration is
enabled.

## Role Variables

### Required variables

```yaml
deploy_user: deploy
install_root: /opt/prodigy

db_host: localhost
application_db_name: prodigy
application_dbuser_name: prodigy
application_dbuser_password: change-me

prodigy_recipe_url: https://example.com/recipe.py
prodigy_recipe_pyfile: /opt/prodigy/muse/recipes/recipe.py

prodigy_datafile_src: /mnt/tigerdata/path/to/tasks.jsonl
prodigy_datafile: /opt/prodigy/muse/data/tasks.jsonl

prodigy_instruct_src: /mnt/tigerdata/path/to/instructions.html
prodigy_instruct: /opt/prodigy/muse/data/instructions.html

nginx_config_file: /etc/nginx/nginx.conf
```


