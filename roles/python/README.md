python
======

Installs a specified version of python and creates a virtual environment. If a `requirements.txt` file is present in the target directory, python dependencies will be installed to the newly created virtual environment.

Requirements
------------

The "project" directory, where the virtual environment will be created, should exist. To specify it, set `python_app_path`. Ensure that `python_user` has permission to modify this directory and its contents.

Role Variables
--------------

- `python_user`: the user account that will run python; should have access to `python_app_path`
- `python_version`: version of python to be installed
- `python_app_path`: location where this version of python will be used
- `python_venv_path`: location to create the virtual environment; optional. default is `python_app_path/env`
- `python_requirements_file`: path to `requirements.txt` file; optional. default is `python_app_path/requirements.txt`

Example Playbook
----------------

```yml
    - hosts: myapp
      roles:
         - { role: python, python_version: "3.8", python_user: "conan" }
```
