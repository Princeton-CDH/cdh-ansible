cdh.common
==========

Installs a basic set of packages on a Ubuntu machine to aid in deployments - see `common_packages` in `defaults/main.yml` for the list of packages. Also configures `tmux` to keep a longer scrollback history.

Example Playbook
----------------

    - hosts: servers
      roles:
         - cdh.common

License
-------

See [LICENSE](https://github.com/Princeton-CDH/CDH_ansible/blob/main/LICENSE).