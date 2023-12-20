# cdhweb setup

Application setup specific to CDH web.

Currently includes handling for licensed fonts. A vaulted archive file of the purchased fonts is included as a tar file, to be copied and extracted to the remote server.

To update the font file:

- decrypt with ansible-vault: `ansible-vault encrypt roles/cdhweb_setup/files/cdhweb_fonts.vault`
- extract files to a temporary directory via `tar -xvf roles/cdhweb_setup/files/cdhweb_fonts.vault`
- add/remove files as needed
- update vault file from the directory with the font files
  via `tar -cvf [path]roles/cdhweb_setup/files/cdhweb_fonts.vault *`  
  (Needs to be included without any folder or additional path.)
- re-encrypt with default vault key `ansible-vault encrypt --encrypt-vault-id default roles/cdhweb_setup/files/cdhweb_fonts.vault`  
