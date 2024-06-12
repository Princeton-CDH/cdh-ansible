#!/usr/bin/env python
"""
Python script to make it easier to work with ansible vault encrypted variable
values in an un-encrypted vars file.  Supports encrypting all values in a yaml
variable file (preserves block comments), decrypting all values (for display only),
and checking that all values in a yaml variable file are encrypted.
"""
import argparse

import os
import re
import subprocess
import sys
import shutil
from pathlib import Path

import yaml
import ansible.cli
from ansible.constants import DEFAULT_VAULT_ID_MATCH
from ansible.parsing.vault import VaultSecret, VaultLib


class VaultedVariable(yaml.YAMLObject):
    """yaml object to handle ansible vault tag"""

    yaml_tag = "!vault"

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.val}>"

    @classmethod
    def from_yaml(cls, loader, node):
        return cls(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(cls.yaml_tag, data.val)


def encrypt_string(value):
    # encrypt a string with vault and decode from binary to string
    # NOTE: depends on vault variable in main namespace
    return vault.encrypt(value).decode()


def decrypt_string(value):
    # decrypt a string with vault and decode from binary to string
    # NOTE: depends on vault variable in main namespace
    return vault.decrypt(value).decode()


def encrypt_yaml_vars(data):
    result = {}
    for name, value in data.items():
        # if a variable is already encrypted, preserve
        if isinstance(value, VaultedVariable):
            result[name] = value
        if isinstance(value, dict):
            result[name] = encrypt_yaml_vars(value)
        else:
            # encrypted the variable value
            val = encrypt_string(value)
            # ansible vault encryption includes line breaks
            # when serialized, they are doubled but encryption
            # results in the correct value.
            # Removing the line breaks results in one long string,
            # and wrapping seems preferable.
            result[name] = VaultedVariable(val)
    return result


def encrypt_vars_in_file(infile):
    filepath = Path(infile)
    backup_file = Path(f"{infile}.bk")
    # check if backup already exists?
    shutil.copyfile(infile, backup_file)

    # collect lines of output
    output = []
    with filepath.open() as varfile:
        content = varfile.read()
        # split by comments so we can parse groups of content together
        content_chunks = re.split(r"(^#.*)$", content, flags=re.M)
        for chunk in content_chunks:
            # comment / whitespace; include in output as-is
            if chunk.startswith("#") or not chunk.strip():
                output.append(chunk)
            else:
                parsed_chunk = yaml.load(chunk, Loader=yaml.Loader)
                output_chunk = encrypt_yaml_vars(parsed_chunk)
                # add a new line before the section
                yaml_output = f"\n{yaml.dump(output_chunk)}"
                output.append(yaml_output)

    print(f"Saving changes to {filepath}; backup is in {backup_file}")
    with filepath.open("w") as varfile:
        varfile.write("".join(output))


def decrypt_vars(data):
    # recursive function to decrypt yaml data with vaulted variables
    result = {}
    for name, value in data.items():
        output_value = value
        if isinstance(value, VaultedVariable):
            # decrypt to get the un-encrypted string
            output_value = decrypt_string(value.val)
        elif isinstance(value, dict):
            output_value = decrypt_vars(value)

        result[name] = output_value
    return result


def decrypt_file_vars(infile):
    output = {}
    # decrypt for now
    with open(infile) as varfile:
        output = decrypt_vars(yaml.load(varfile, Loader=yaml.Loader))

    print(f"\nVariables from {infile}:")
    yaml.dump(output, sys.stdout)


def check_vars_encrypted(data):
    # if file is fully vaulted, it will load as a single string
    if not isinstance(data, dict):
        raise ValueError("Error parsing as yaml")
    ok = []

    for name, value in data.items():
        if isinstance(value, dict):
            ok.append(check_vars_encrypted(value))
        elif isinstance(value, VaultedVariable):
            ok.append(True)
        else:
            print(f"{name} is not encrypted")
            ok.append(False)

    return all(ok)


def check_file_vars_encrypted(infile, quiet=False):
    with open(infile) as varfile:
        try:
            ok = check_vars_encrypted(yaml.load(varfile, Loader=yaml.Loader))
            if ok:
                if not quiet:
                    print(f"✅ {infile}: all variables are encrypted")
            else:
                print(f"⚠️ {infile} has unencrypted variables")

            return ok
        except:
            print(f"❗️{infile} error parsing as yaml; is this file encrypted?")
            return False


def init_vault():
    # initialize ansible VaultLib with vault secret for encrypt/decrypt
    vault_id = os.environ.get("ANSIBLE_VAULT_IDENTITY_LIST")
    # NOTE: currently only supports the configuration documented in the README
    # split the vault id from the command and run the command to generate the secret
    result = subprocess.run([vault_id.split("@")[1]], capture_output=True)
    secret = result.stdout.strip()  # remove trailing newline
    # TODO: use cli.vault code?
    # initialize VaultLib object with list of tuples of vault id, vault secret
    return VaultLib([("default", VaultSecret(secret))])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ansible vault variables values in a yaml file"
    )
    parser.add_argument(
        "mode",
        help="action: encrypt variables, decrypt and report, or "
        + "check that all variables are encrypted",
        choices=["encrypt", "decrypt", "check"],
    )
    parser.add_argument(
        "-q",
        "--quiet",
        default=False,
        help="less verbose output",
        action="store_true",
    )
    parser.add_argument("file", help="variable file(s) to work with", nargs="*")

    args = parser.parse_args()

    # initialize vault if needed (not needed if mode = check)
    if args.mode in ["encrypt", "decrypt"]:
        vault = init_vault()

    # encrypt mode: update all files to encrypt variables
    if args.mode == "encrypt":
        for infile in args.file:
            encrypt_vars_in_file(infile)
        print(
            "Encrypted variables in place. "
            + "Be sure to check comments for any sensitive information."
        )

    elif args.mode == "check":
        ok = []
        for infile in args.file:
            ok.append(check_file_vars_encrypted(infile, quiet=args.quiet))
            if not all(ok):
                raise SystemExit(-1)

    elif args.mode == "decrypt":
        for infile in args.file:
            decrypt_file_vars(infile)
