#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

# Exec the specified command or fall back on bash
if [ $# -eq 0 ]; then
    cmd=( "bash" )
else
    cmd=( "$@" )
fi

# The run-hooks function looks for .sh scripts and executable files
# - .sh scripts will be sourced
# - executable files (+x) will be executed
run-hooks () {
    if [[ ! -d "${1}" ]] ; then
        return
    fi
    echo "${0}: running hooks in ${1} as uid / gid: $(id -u) / $(id -g)"
    for f in "${1}/"*; do
        case "${f}" in
            *.sh)
                echo "${0}: running script ${f}"
                # shellcheck disable=SC1090
                source "${f}"
                ;;
            *)
                if [[ -x "${f}" ]] ; then
                    echo "${0}: running executable ${f}"
                    "${f}"
                else
                    echo "${0}: ignoring non-executable ${f}"
                fi
                ;;
        esac
    done
    echo "${0}: done running hooks in ${1}"
}



# NOTE: This hook will run as the user the container was started with!
run-hooks /usr/local/bin/start-notebook.d



# If we have started the container as the root user, then we have permission to
# manipulate user identities and storage file permissions before we start the
# server as a non-root user.
#
# Environment variables of relevance:
# - NB_UID: the user we want to run as, uniquely identified by an id
# - NB_USER: the username and associated home folder we want for our user
# - NB_GID: a group we want our user to belong to, uniquely identified by an id
# - NB_GROUP: the groupname we want for the group
if [ "$(id -u)" == 0 ] ; then

    # Optionally ensure the user we want to run as (NB_UID) get filesystem
    # ownership of it's home folder and additional folders. This can be relevant
    # for attached NFS storage.
    #
    # Environment variables:
    # - CHOWN_HOME: a boolean ("1" or "yes") to chown the user's home folder
    # - CHOWN_EXTRA: a comma separated list of paths to chown
    # - CHOWN_HOME_OPTS / CHOWN_EXTRA_OPTS: arguments to the chown command
    if [[ "${CHOWN_HOME}" == "1" || "${CHOWN_HOME}" == "yes" ]]; then
        echo "Updating ownership of /home/${NB_USER} to ${NB_UID}:${NB_GID} with options '${CHOWN_HOME_OPTS}'"
        # shellcheck disable=SC2086
        chown $CHOWN_HOME_OPTS "${NB_UID}:${NB_GID}" "/home/${NB_USER}"
    fi
    if [ -n "${CHOWN_EXTRA}" ]; then
        for extra_dir in $(echo "${CHOWN_EXTRA}" | tr ',' ' '); do
            echo "Updating ownership of ${extra_dir} to ${NB_UID}:${NB_GID} with options '${CHOWN_EXTRA_OPTS}'"
            # shellcheck disable=SC2086
            chown ${CHOWN_EXTRA_OPTS} "${NB_UID}:${NB_GID}" "${extra_dir}"
        done
    fi

    # Update the jovyan identity to get desired username and its associated home folder.
    if id jovyan &> /dev/null ; then
        echo "Updating the default jovyan user:"
        echo "username: jovyan -> ${NB_USER}"
        echo "home dir: /home/jovyan -> /home/${NB_USER}"
        usermod --home "/home/${NB_USER}" --login "${NB_USER}" jovyan
    fi
    # Update any environment variables we set during build of the
    # Dockerfile that contained the home directory path.
    export XDG_CACHE_HOME=/home/$NB_USER/.cache

    # For non-jovyan username's, populate their home directory with the jovyan's
    # home directory as a fallback if they don't have one mounted already.
    if [[ "${NB_USER}" != "jovyan" ]]; then
        if [[ ! -e "/home/${NB_USER}" ]]; then
            echo "Attempting to copy /home/jovyan to /home/${NB_USER}..."
            mkdir "/home/${NB_USER}"
            if cp -a /home/jovyan/. "/home/${NB_USER}/"; then
                echo "Done"
            else
                echo "Failed. Attempting to symlink /home/jovyan to /home/${NB_USER}..."
                ln -s /home/jovyan "/home/${NB_USER}" && echo "Done"
            fi
        fi
        # Ensure the current working directory is updated
        if [[ "${PWD}/" == "/home/jovyan/"* ]]; then
            newcwd="/home/${NB_USER}/${PWD:13}"
            echo "Changing working directory to ${newcwd}"
            cd "${newcwd}"
        fi
    fi

    # Ensure NB_USER gets the NB_UID user id and is a member of the NB_GID group
    if [ "${NB_UID}" != "$(id -u "${NB_USER}")" ] || [ "${NB_GID}" != "$(id -g "${NB_USER}")" ]; then
        echo "Update ${NB_USER}'s UID:GID to ${NB_UID}:${NB_GID}"
        # Ensure the group's existence
        if [ "${NB_GID}" != "$(id -g "${NB_USER}")" ]; then
            groupadd --force --gid "$NB_GID" --non-unique "${NB_GROUP:-${NB_USER}}"
        fi
        # Recreate the user as we want it
        userdel "${NB_USER}"
        useradd --home "/home/${NB_USER}" --uid "${NB_UID}" --gid "${NB_GID}" --groups 100 --no-log-init "${NB_USER}"
    fi

    # Conditionally enable passwordless sudo usage for the jovyan user
    if [[ "${GRANT_SUDO}" == "1" || "${GRANT_SUDO}" == 'yes' ]]; then
        echo "Granting ${NB_USER} passwordless sudo rights!"
        echo "${NB_USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/added-by-start-script
    fi

    # Ensure that the initial environment that this container is started with
    # is preserved when we run transition from running as root to running as
    # NB_USER.
    #
    # - We use the sudo command to execute the command as NB_USER. But, what
    #   happens to the environment will be determined by configuration in
    #   /etc/sudoers and /etc/sudoers.d/* as well as flags we pass to the sudo
    #   command. The behavior can be inspected with `sudo -V` run as root.
    #
    #   ref: `man sudo` - https://linux.die.net/man/8/sudo ref: `man sudoers` -
    #   https://www.sudo.ws/man/1.8.15/sudoers.man.html
    #
    # - We use the `--preserve-env` flag to pass through most environment, but
    #   understand that exceptions are caused by the sudoers configuration:
    #   `env_delete`, `env_check`, and `secure_path`.
    #
    # - We reduce the `env_delete` list of default variables to be deleted by
    #   default which would ignore the `--preserve-env` flag and `env_keep`
    #   configuration.
    #
    # - We manage the PATH variable specifically as `secure_path` is set by
    #   default in /etc/sudoers and would override the PATH variable. So we
    #   disable that default.
    echo 'Defaults env_delete -= "PATH LD_* PYTHON*"' >> /etc/sudoers.d/added-by-start-script
    echo 'Defaults !secure_path' >> /etc/sudoers.d/added-by-start-script

    # NOTE: This hook is run as the root user!
    run-hooks /usr/local/bin/before-notebook.d

    echo "Running as ${NB_USER}:" "${cmd[@]}"
    exec sudo --preserve-env --set-home --user "${NB_USER}" "${cmd[@]}"



# The container didn't start as the root user.
else
    if [[ "${NB_UID}" == "$(id -u jovyan 2>/dev/null)" && "${NB_GID}" == "$(id -g jovyan 2>/dev/null)" ]]; then
        # User is not attempting to override user/group via environment
        # variables, but they could still have overridden the uid/gid that
        # container runs as. Check that the user has an entry in the passwd
        # file and if not add an entry.
        STATUS=0 && whoami &> /dev/null || STATUS=$? && true
        if [[ "${STATUS}" != "0" ]]; then
            if [[ -w /etc/passwd ]]; then
                echo "Adding passwd file entry for $(id -u)"
                sed -e "s/^jovyan:/nayvoj:/" /etc/passwd > /tmp/passwd
                echo "jovyan:x:$(id -u):$(id -g):,,,:/home/jovyan:/bin/bash" >> /tmp/passwd
                cat /tmp/passwd > /etc/passwd
                rm /tmp/passwd
            else
                echo "WARNING: Container must be run with group 'root' to update passwd file"
            fi
        fi

        # Warn if the user isn't going to be able to write files to ${HOME}.
        if [[ ! -w /home/jovyan ]]; then
            echo "WARNING: Container must be run with group 'users' to update files"
        fi
    else
        # Warn if looks like user want to override uid/gid but hasn't
        # run the container as root.
        if [[ -n "${NB_UID}" && "${NB_UID}" != "$(id -u)" ]]; then
            echo "Container must be run as root to set NB_UID to ${NB_UID}"
        fi
        if [[ -n "${NB_GID}" && "${NB_GID}" != "$(id -g)" ]]; then
            echo "Container must be run as root to set NB_GID to ${NB_GID}"
        fi
    fi

    # Warn about a probable misconfiguration of sudo
    if [[ "${GRANT_SUDO}" == "1" || "${GRANT_SUDO}" == 'yes' ]]; then
        echo "WARNING: container must be started up as root to grant sudo permissions."
    fi

    run-hooks /usr/local/bin/before-notebook.d
    echo "Executing the command:" "${cmd[@]}"
    exec "${cmd[@]}"
fi
