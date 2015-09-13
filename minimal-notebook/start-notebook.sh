#!/bin/bash

# Change UID of jovyan to NB_UID if it does not match
if [ "$NB_UID" != $(id -u jovyan) ] ; then
    usermod -u $NB_UID $NB_USER
    chown -R $NB_UID $CONDA_DIR
fi

# Enable sudo if requested
if [ ! -z "$GRANT_SUDO" ]; then
    echo "$NB_USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook
fi

# Start supervisord in foreground, PID1
exec supervisord -n -c /etc/supervisor/supervisord.conf
