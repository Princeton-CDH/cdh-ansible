# VM Software and Versioning

This is a table of the versions of SCL packages on various CDH VMs for guidance
in writing and maintaining playbooks. If in doubt, you can also log into a
VM and run `scl -l` to see available SCLs.

Other versions present on the server are listed in parentheses.

QA has all of these versions available, but uses
rh-python35 for its python with Apache ()


| VM               | rh-pythonX | node-jsX     |
| -----------------| -----------| -------------|
| cdh-web          | 35         | 10 (6)       |
| derridas-margins | 35         | 6            |
| mep              | 35         | 8 (10)       |
| ppa              | 36         | 8 (10, 6)    |
| winthrop         | 35         | 8            |
