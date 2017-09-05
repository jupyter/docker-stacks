#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

# Handle special flags if we're root
if [ $(id -u) == 0 ] ; then
    # Switch to the root of the container in case we start adjusting paths
    # that impact the default working directory
    cd /

    # Handle username change. Since this is cheap, do this unconditionally
    echo "Set username to: $NB_USER"
    usermod -m -d /home/$NB_USER -l $NB_USER jovyan

    # Change UID of NB_USER to NB_UID if it does not match
    if [ "$NB_UID" != $(id -u $NB_USER) ] ; then
        echo "Set $NB_USER UID to: $NB_UID"
        usermod -u $NB_UID $NB_USER
    fi

    # Change GID of NB_USER to NB_GID if NB_GID is passed as a parameter
    if [ "$NB_GID" ] ; then
        echo "Set $NB_USER GID to: $NB_GID"
        groupmod -g $NB_GID -o $(id -g -n $NB_USER)
    fi

    # Enable sudo if requested
    if [[ "$GRANT_SUDO" == "1" || "$GRANT_SUDO" == 'yes' ]]; then
        echo "Granting $NB_USER sudo access"
        echo "$NB_USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook
    fi

    # Switch to the user's home directory after adjusting any paths
    cd /home/$NB_USER

    # Exec the command as NB_USER
    echo "Execute the command: $*"
    exec su $NB_USER -c "env PATH=$PATH $*"
else
  if [[ ! -z "$NB_UID" && "$NB_UID" != "$(id -u)" ]]; then
      echo 'Container must be run as root to set $NB_UID'
  fi
  if [[ ! -z "$NB_GID" && "$NB_GID" != "$(id -g)" ]]; then
      echo 'Container must be run as root to set $NB_GID'
  fi
  if [[ "$GRANT_SUDO" == "1" || "$GRANT_SUDO" == 'yes' ]]; then
      echo 'Container must be run as root to grant sudo permissions'
  fi
    # Exec the command
    echo "Execute the command: $*"
    exec $*
fi
