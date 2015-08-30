#!/bin/bash

# Constants
NB_USER=jovyan
NB_HOME=/home/$NB_USER
NB_WORK=$NB_HOME/work

# Create non-root NB_USER if one doesn't exist
id -u $NB_USER && user_exists=true
if [ -z "$user_exists" ] ; then
    useradd -m -s /bin/bash -u ${NB_UID:-1000} $NB_USER

    # Setup a work directory rooted in the NB_USER home
    mkdir -p $NB_WORK
    chown -R $NB_USER.$NB_USER $NB_HOME

    # Allow NB_USER group to update conda root env
    chown -R root.$NB_USER $CONDA_DIR
    chmod g+w $CONDA_DIR
fi

# Copy skeleton files if useradd didn't do it (e.g., volume mounted dir
# residing in NB_HOME prevented it)
if [ ! -d $NB_HOME/.jupyter ]; then
    cp -r /etc/skel/. $NB_HOME
    chown -R $NB_USER.$NB_USER $NB_HOME
fi

# Enable sudo if requested
if [ ! -z "$GRANT_SUDO" ]; then
    echo "$NB_USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook
fi

# Start supervisord in foreground, PID1
exec supervisord -n -c /etc/supervisor/supervisord.conf
