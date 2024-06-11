# Use vaulted variables in group vars instead of encrypting entire files

* Status: accepted
* Deciders: @rlskoeser, @acozine
* Date: 2024-06-11

## Context and Problem Statement

CDH ansible inventory uses group variables, including vaulted variables (fully encrypted `vault.yml) for sensitive configurations. This prevents Ansible Tower from importing the inventory, since the inventory includes not only hostnames and groups but also group variables. The Ansible Tower inventory import task does not and should have access to the vault password; this is intentional, because if it decryted on import, then sensitive configurations would be stored in plain text in the Ansible Tower inventory.

## Decision 

Switch from encrypting entire `vault.yml` files to only encrypting the values of sensitive variables ([see Ansible documentation on encrypting invidual variables](https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#encrypting-individual-variables-with-ansible-vault). 

### Positive Consequences 

* Inventory can be successfully loaded in Ansible Tower without compromising sensitive configuration values
* We can continue to use group variables and shared host groups as before
* The same setup can be used to run playbooks and load inventory ang group variables in both Ansible Tower and local installations
* Vaulted variable files can be inspected to see variable names and comments without fully decrypting 

### Negative Consequences 

* Encrypting and decrypting variables is slightly more complicated than before, since the `ansible-vault` script only handles encrypting a string and not encrypting or decrypting mutiple values in a file. We mitigate this by adding a custom python script to assist with encrypting all variables in a file, decrypting variables for view, and 
to check that all variables in a `vault.yml` group vars file are encrypted.