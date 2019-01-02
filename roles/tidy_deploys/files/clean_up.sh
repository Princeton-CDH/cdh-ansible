#!/bin/bash
# This script looks for the INSTALL_BASE directory of
# a project and then deletes all but the two most recent
# directories using the piped command
# Usage: clean_up.sh INSTALL_BASE


INSTALL_BASE=$1

# check if the install base looks valid
# i.e., is in /srv/www
if [[ $INSTALL_BASE != /srv/www* ]]; then
    echo "Install base not in /srv/www, aborting!"
    exit 1
fi

cd $INSTALL_BASE

if [[ `pwd` != $INSTALL_BASE ]]; then
    echo "Did not change to INSTALL_BASE, aborting!"
    exit 1
fi

# Assuming we did not exit above, perform the following
# - find all directories one level deep
# - not named: media, "log*" or "font*"
# - print them in a tab delimited format that leads with timestamp
# - sort them in reverse order to get most recent first
# - delete the first two entries (two most recent) via sed
# - print out a tab delimited list of folder names only
# - use xargs to pipe output as a list of folders to delete
find . -mindepth 1 -maxdepth 1 \
        -type d ! -name media ! -name "log*" ! -name "font*" \
        -printf "%T@\t%Tc\t%p\n" \
        | sort -nr | sed -e "1,2d" \
        | awk -F $'\t' '{print $3}' \
        | xargs rm -rf
