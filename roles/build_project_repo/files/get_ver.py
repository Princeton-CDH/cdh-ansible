#!/usr/bin/env python
'''
This shim script loads a Django application (or any app)
that has a __version__ variable.
It takes two variables and depends on system Python 2 or 3

Usage: ger_ver.py repo_path app_name
'''
import sys
import importlib


def main(repo_path, app_name):
    # add the Django module to syspath
    sys.path.append(repo_path)
    # use importlib to load the module
    app = importlib.import_module(app_name)
    # write version to stdout to capture in Ansible
    sys.stdout.write(app.__version__)


if __name__ == '__main__':
    # sysargs 1 and 2 to repo_path
    repo_path = sys.argv[1]
    app_name = sys.argv[2]
    # run main
    main(repo_path, app_name)
