# Templates

The templates folder contains files related to deploys that are rendered on
the remote system using Ansible's template module.

Since Python uses `{{}}` as a standard character, there are overlaps in config
files and the Jinja2 templating system used in Ansible (which) reads the config
as a string.

These files therefore use a modified `^^ ^^` syntax to denote a variable. Any
variable used in the templated file
(and any reference it makes to vault variables) must use this alternate print
marker. Any role that templates should use these markers for `variable_end_string`
and `variable_start_string`.

Local settings files are in folders namespaced for the name of the group used
in the particular playbook, i.e. `templates/winthrop_qa`
