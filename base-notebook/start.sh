#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

# Handle special flags if we're root
if [ $UID == 0 ] ; then
    # Change UID of NB_USER to NB_UID if it does not match
    if [ "$NB_UID" != $(id -u $NB_USER) ] ; then
        usermod -u $NB_UID $NB_USER
        # Careful: $HOME might resolve to /root depending on how the
        # container is started. Use the $NB_USER home path explicitly.
        for d in "$CONDA_DIR" "$JULIA_PKGDIR" "/home/$NB_USER"; do
            if [[ ! -z "$d" && -d "$d" ]]; then
                chown -R $NB_UID "$d"
            fi
        done
    fi

    # Change GID of NB_USER to NB_GID if NB_GID is passed as a parameter
    if [ "$NB_GID" ] ; then
        groupmod -g $NB_GID -o $(id -g -n $NB_USER)
    fi

    # Enable sudo if requested
    if [ ! -z "$GRANT_SUDO" ]; then
        # Ensure includedir sudoers.d is not commented
        sed -i -E 's|^#(includedir /etc/sudoers.d.*)|\1|g' /etc/sudoers
        echo "$NB_USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook
    fi

    # Exec the command as NB_USER
    exec su $NB_USER -c "env PATH=$PATH $*"
else
    # Exec the command
    exec $*
fi
