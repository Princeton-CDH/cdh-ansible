geniza_setup
============

Application setup specific to geniza playbooks.

Currently includes handling for licensed fonts. A vaulted archive file of the purchased fonts is included as a tar file, to be copied and extracted to the remote server.

To update the font file:

- extract files to a temporary directory via `tar -xvf roles/geniza_setup/files/geniza_fonts.vault`
- add/remove files as needed
- update vault file from the directory with the font files
  via `tar -cvf [path]roles/geniza_setup/files/ *`  
  (Needs to be included without any folder or additional path.)
