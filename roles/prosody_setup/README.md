prosody setup
==============

Application setup specific to prosody (PPA) playbooks.

Currently includes steps to ensure that configured directories 
HathiTrust data and Gale/ECCO MARC data exist, with an optional task 
to extract MARC records if they are not present.

This role includes a vaulted archive (tar + bzip2) with the binary MARC 
records, so they can be extracted on the target server if needed.

If you need to do any work with the the vaulted tar file:

- decrypt with ansible-vault: `ansible-vault encrypt files/ecco_marc.vault`
- extract files to a temporary directory via `tar -xvjf roles/prosody_setup/files/ecco_marc.vault`
- add/remove files as needed
- update vault file from the directory with the font files
  via `tar -cvjf [path]roles/geniza_setup/files/ecco_marc.vault *`  
  (Needs to be included without any folder or additional path.)
