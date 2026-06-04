# geniza_setup

Setup specific to geniza application.

Currently includes handling for licensed fonts. A vaulted archive file of the purchased fonts is included as a tar file, to be copied and extracted to the remote server.

This role also includes the setup for github access, git configuration, and data directory needed for pushing data exports from the web application to GitHub.

To update the font file:

- from the `cdh-ansible` project root, decrypt the vault file:
  ```sh
  ansible-vault decrypt roles/geniza_setup/files/geniza_fonts.vault
  ```
- extract files to a temporary directory, for example `geniza_fonts`:
  ```sh
  cd .. && mkdir geniza_fonts && cd geniza_fonts
  tar -xvf ../cdh-ansible/roles/geniza_setup/files/geniza_fonts.vault
  ```
- add/remove any font files in the new `geniza_fonts` directory
- repack it into the vault file and re-encrypt:
  ```sh
  tar -cvf ../cdh-ansible/roles/geniza_setup/files/geniza_fonts.vault *
  cd ../cdh-ansible
  ansible-vault encrypt roles/geniza_setup/files/geniza_fonts.vault
  ```

Then open a pull request to update this repo, so that the new font file can be used in future playbook runs.
