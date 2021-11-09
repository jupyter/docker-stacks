#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e
echo "Running: start.sh" "$@"

# Exec the specified command or fall back on bash
if [ $# -eq 0 ]; then
    cmd=( "bash" )
else
    cmd=( "$@" )
fi

# The run-hooks function looks for .sh scripts to source and executable files to
# run within a passed directory.
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

# If the container started as the root user, then we have permission to refit
# the jovyan user, and ensure file permissions, grant sudo rights, and such
# things before we run the command passed to start.sh as the desired user
# (NB_USER).
#
if [ "$(id -u)" == 0 ] ; then
    # Environment variables:
    # - NB_USER: the desired username and associated home folder
    # - NB_UID: the desired user id
    # - NB_GID: a group id we want our user to belong to
    # - NB_GROUP: the groupname we want for the group
    # - GRANT_SUDO: a boolean ("1" or "yes") to grant the user sudo rights
    # - CHOWN_HOME: a boolean ("1" or "yes") to chown the user's home folder
    # - CHOWN_EXTRA: a comma separated list of paths to chown
    # - CHOWN_HOME_OPTS / CHOWN_EXTRA_OPTS: arguments to the chown commands

    # Refit the jovyan user to the desired the user (NB_USER)
    if id jovyan &> /dev/null ; then
        if ! usermod --home "/home/${NB_USER}" --login "${NB_USER}" jovyan 2>&1 | grep "no changes" > /dev/null; then
            echo "Updated the jovyan user:"
            echo "- username: jovyan       -> ${NB_USER}"
            echo "- home dir: /home/jovyan -> /home/${NB_USER}"
        fi
    elif ! id -u "${NB_USER}" &> /dev/null; then
        echo "ERROR: Neither the jovyan user or '${NB_USER}' exists."
        echo "       This could be the result of stopping and starting, the"
        echo "       container with a different NB_USER environment variable."
        exit 1
    fi
    # Ensure the desired user (NB_USER) gets its desired user id (NB_UID) and is
    # a member of the desired group (NB_GROUP, NB_GID)
    if [ "${NB_UID}" != "$(id -u "${NB_USER}")" ] || [ "${NB_GID}" != "$(id -g "${NB_USER}")" ]; then
        echo "Update ${NB_USER}'s UID:GID to ${NB_UID}:${NB_GID}"
        # Ensure the desired group's existence
        if [ "${NB_GID}" != "$(id -g "${NB_USER}")" ]; then
            groupadd --force --gid "${NB_GID}" --non-unique "${NB_GROUP:-${NB_USER}}"
        fi
        # Recreate the desired user as we want it
        userdel "${NB_USER}"
        useradd --home "/home/${NB_USER}" --uid "${NB_UID}" --gid "${NB_GID}" --groups 100 --no-log-init "${NB_USER}"
    fi

    # Move or symlink the jovyan home directory to the desired users home
    # directory if it doesn't already exist, and update the current working
    # directory to the new location if needed.
    if [[ "${NB_USER}" != "jovyan" ]]; then
        if [[ ! -e "/home/${NB_USER}" ]]; then
            echo "Attempting to copy /home/jovyan to /home/${NB_USER}..."
            mkdir "/home/${NB_USER}"
            if cp -a /home/jovyan/. "/home/${NB_USER}/"; then
                echo "Success!"
            else
                echo "Failed!"
                echo "Attempting to symlink /home/jovyan to /home/${NB_USER}..."
                if ln -s /home/jovyan "/home/${NB_USER}"; then
                    echo "Success!"
                else
                    echo "Failed!"
                fi
            fi
        fi
        # Ensure the current working directory is updated to the new path
        if [[ "${PWD}/" == "/home/jovyan/"* ]]; then
            new_wd="/home/${NB_USER}/${PWD:13}"
            echo "Changing working directory to ${new_wd}"
            cd "${new_wd}"
        fi
    fi

    # Optionally ensure the desired user get filesystem ownership of it's home
    # folder and/or additional folders
    if [[ "${CHOWN_HOME}" == "1" || "${CHOWN_HOME}" == "yes" ]]; then
        echo "Ensuring /home/${NB_USER} is owned by ${NB_UID}:${NB_GID} ${CHOWN_HOME_OPTS:+(chown options: ${CHOWN_HOME_OPTS})}"
        # shellcheck disable=SC2086
        chown ${CHOWN_HOME_OPTS} "${NB_UID}:${NB_GID}" "/home/${NB_USER}"
    fi
    if [ -n "${CHOWN_EXTRA}" ]; then
        for extra_dir in $(echo "${CHOWN_EXTRA}" | tr ',' ' '); do
            echo "Ensuring ${extra_dir} is owned by ${NB_UID}:${NB_GID} ${CHOWN_HOME_OPTS:+(chown options: ${CHOWN_HOME_OPTS})}"
            # shellcheck disable=SC2086
            chown ${CHOWN_EXTRA_OPTS} "${NB_UID}:${NB_GID}" "${extra_dir}"
        done
    fi

    # Update potentially outdated environment variables since image build
    export XDG_CACHE_HOME="/home/${NB_USER}/.cache"

    # Add ${CONDA_DIR}/bin to sudo secure_path
    sed -r "s#Defaults\s+secure_path\s*=\s*\"?([^\"]+)\"?#Defaults secure_path=\"\1:${CONDA_DIR}/bin\"#" /etc/sudoers | grep secure_path > /etc/sudoers.d/path

    # Optionally grant passwordless sudo rights for the desired user
    if [[ "$GRANT_SUDO" == "1" || "$GRANT_SUDO" == "yes" ]]; then
        echo "Granting ${NB_USER} passwordless sudo rights!"
        echo "${NB_USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/added-by-start-script
    fi

    # NOTE: This hook is run as the root user!
    run-hooks /usr/local/bin/before-notebook.d

    echo "Running as ${NB_USER}:" "${cmd[@]}"
    exec sudo --preserve-env --set-home --user "${NB_USER}" \
        PATH="${PATH}" XDG_CACHE_HOME="/home/${NB_USER}/.cache" \
        PYTHONPATH="${PYTHONPATH:-}" \
        "${cmd[@]}"

# The container didn't start as the root user, so we will have to act as the
# user we started as.
else
    # Warn about misconfiguration of: desired username, user id, or group id
    if [[ -n "${NB_USER}" && "${NB_USER}" != "$(id -un)" ]]; then
        echo "WARNING: container must be started as root to change the desired user's name with NB_USER!"
    fi
    if [[ -n "${NB_UID}" && "${NB_UID}" != "$(id -u)" ]]; then
        echo "WARNING: container must be started as root to change the desired user's id with NB_UID!"
    fi
    if [[ -n "${NB_GID}" && "${NB_GID}" != "$(id -g)" ]]; then
        echo "WARNING: container must be started as root to change the desired user's group id with NB_GID!"
    fi

    # Warn about misconfiguration of: granting sudo rights
    if [[ "${GRANT_SUDO}" == "1" || "${GRANT_SUDO}" == "yes" ]]; then
        echo "WARNING: container must be started as root to grant sudo permissions!"
    fi

    # Attempt to ensure the user uid we currently run as has a named entry in
    # the /etc/passwd file, as it avoids software crashing on hard assumptions
    # on such entry. Writing to the /etc/passwd was allowed for the root group
    # from the Dockerfile during build.
    #
    # ref: https://github.com/jupyter/docker-stacks/issues/552
    if ! whoami &> /dev/null; then
        echo "There is no entry in /etc/passwd for our UID. Attempting to fix..."
        if [[ -w /etc/passwd ]]; then
            echo "Renaming old jovyan user to nayvoj ($(id -u jovyan):$(id -g jovyan))"
            sed --in-place "s/^jovyan:/nayvoj:/" /etc/passwd

            echo "jovyan:x:$(id -u):$(id -g):,,,:/home/jovyan:/bin/bash" >> /etc/passwd
            echo "Added new jovyan user ($(id -u):$(id -g)). Fixed UID!"
        else
            echo "WARNING: unable to fix missing /etc/passwd entry because we don't have write permission."
        fi
    fi

    # Warn if the user isn't able to write files to ${HOME}
    if [[ ! -w /home/jovyan ]]; then
        echo "WARNING: no write access to /home/jovyan. Try starting the container with group 'users' (100)."
    fi

    # NOTE: This hook is run as the user we started the container as!
    run-hooks /usr/local/bin/before-notebook.d
    echo "Executing the command:" "${cmd[@]}"
    exec "${cmd[@]}"
fi
