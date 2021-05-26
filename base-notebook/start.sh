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

run-hooks () {
    # Source scripts or run executable files in a directory
    if [[ ! -d "${1}" ]] ; then
        return
    fi
    echo "${0}: running hooks in ${1}"
    for f in "${1}/"*; do
        case "${f}" in
            *.sh)
                echo "${0}: running ${f}"
                # shellcheck disable=SC1090
                source "${f}"
                ;;
            *)
                if [[ -x "${f}" ]] ; then
                    echo "${0}: running ${f}"
                    "${f}"
                else
                    echo "${0}: ignoring ${f}"
                fi
                ;;
        esac
    done
    echo "${0}: done running hooks in ${1}"
}

run-hooks /usr/local/bin/start-notebook.d

# Handle special flags if we're root
if [ "$(id -u)" == 0 ] ; then

    # Only attempt to change the jovyan username if it exists
    if id jovyan &> /dev/null ; then
        echo "Set username to: ${NB_USER}"
        usermod -d "/home/${NB_USER}" -l "${NB_USER}" jovyan
    fi

    # handle home and working directory if the username changed
    if [[ "${NB_USER}" != "jovyan" ]]; then
        # changing username, make sure homedir exists
        # (it could be mounted, and we shouldn't create it if it already exists)
        if [[ ! -e "/home/${NB_USER}" ]]; then
            echo "Relocating home dir to /home/${NB_USER}"
            mv /home/jovyan "/home/${NB_USER}" || ln -s /home/jovyan "/home/${NB_USER}"
        fi
        # if workdir is in /home/jovyan, cd to /home/${NB_USER}
        if [[ "${PWD}/" == "/home/jovyan/"* ]]; then
            newcwd="/home/${NB_USER}/${PWD:13}"
            echo "Setting CWD to ${newcwd}"
            cd "${newcwd}"
        fi
    fi

    # Handle case where provisioned storage does not have the correct permissions by default
    # Ex: default NFS/EFS (no auto-uid/gid)
    if [[ "${CHOWN_HOME}" == "1" || "${CHOWN_HOME}" == 'yes' ]]; then
        echo "Changing ownership of /home/${NB_USER} to ${NB_UID}:${NB_GID} with options '${CHOWN_HOME_OPTS}'"
        # shellcheck disable=SC2086
        chown ${CHOWN_HOME_OPTS} "${NB_UID}:${NB_GID}" "/home/${NB_USER}"
    fi
    if [ -n "${CHOWN_EXTRA}" ]; then
        for extra_dir in $(echo "${CHOWN_EXTRA}" | tr ',' ' '); do
            echo "Changing ownership of ${extra_dir} to ${NB_UID}:${NB_GID} with options '${CHOWN_EXTRA_OPTS}'"
            # shellcheck disable=SC2086
            chown ${CHOWN_EXTRA_OPTS} "${NB_UID}:${NB_GID}" "${extra_dir}"
        done
    fi

    # Change UID:GID of NB_USER to NB_UID:NB_GID if it does not match
    if [ "${NB_UID}" != "$(id -u "${NB_USER}")" ] || [ "${NB_GID}" != "$(id -g "${NB_USER}")" ]; then
        echo "Set user ${NB_USER} UID:GID to: ${NB_UID}:${NB_GID}"
        if [ "${NB_GID}" != "$(id -g "${NB_USER}")" ]; then
            groupadd -f -g "${NB_GID}" -o "${NB_GROUP:-${NB_USER}}"
        fi
        userdel "${NB_USER}"
        useradd --home "/home/${NB_USER}" -u "${NB_UID}" -g "${NB_GID}" -G 100 -l "${NB_USER}"
    fi

    # Enable sudo if requested
    if [[ "${GRANT_SUDO}" == "1" || "${GRANT_SUDO}" == 'yes' ]]; then
        echo "Granting ${NB_USER} sudo access and appending ${CONDA_DIR}/bin to sudo PATH"
        echo "${NB_USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook
    fi

    # Add ${CONDA_DIR}/bin to sudo secure_path
    sed -r "s#Defaults\s+secure_path\s*=\s*\"?([^\"]+)\"?#Defaults secure_path=\"\1:${CONDA_DIR}/bin\"#" /etc/sudoers | grep secure_path > /etc/sudoers.d/path

    # Exec the command as NB_USER with the PATH and the rest of
    # the environment preserved
    run-hooks /usr/local/bin/before-notebook.d
    echo "Executing the command:" "${cmd[@]}"
    exec sudo -E -H -u "${NB_USER}" PATH="${PATH}" XDG_CACHE_HOME="/home/${NB_USER}/.cache" PYTHONPATH="${PYTHONPATH:-}" "${cmd[@]}"
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
                echo 'Container must be run with group "root" to update passwd file'
            fi
        fi

        # Warn if the user isn't going to be able to write files to ${HOME}.
        if [[ ! -w /home/jovyan ]]; then
            echo 'Container must be run with group "users" to update files'
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

    # Warn if looks like user want to run in sudo mode but hasn't run
    # the container as root.
    if [[ "${GRANT_SUDO}" == "1" || "${GRANT_SUDO}" == 'yes' ]]; then
        echo 'Container must be run as root to grant sudo permissions'
    fi

    # Execute the command
    run-hooks /usr/local/bin/before-notebook.d
    echo "Executing the command:" "${cmd[@]}"
    exec "${cmd[@]}"
fi
