#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# identical _log to start.sh
# only used when _not_ sourced from start.sh (i.e. unittests)
if ! declare -F _log > /dev/null; then
    _log () {
        if [[ "$*" == "ERROR:"* ]] || [[ "$*" == "WARNING:"* ]] || [[ "${JUPYTER_DOCKER_STACKS_QUIET}" == "" ]]; then
            echo "$@" >&2
        fi
    }
fi

# The run-hooks.sh script looks for *.sh scripts to source
# and executable files to run within a passed directory

if [ "$#" -ne 1 ]; then
    _log "ERROR: Should pass exactly one directory"
    return 1
fi

if [[ ! -d "${1}" ]]; then
    _log "ERROR: Directory ${1} doesn't exist or is not a directory"
    return 1
fi

_log "Running hooks in: ${1} as uid: $(id -u) gid: $(id -g)"
for f in "${1}/"*; do
    # Handling a case when the directory is empty
    [ -e "${f}" ] || continue
    case "${f}" in
        *.sh)
            _log "Sourcing shell script: ${f}"
            # shellcheck disable=SC1090
            source "${f}"
            # shellcheck disable=SC2181
            if [ $? -ne 0 ]; then
                _log "ERROR: ${f} has failed, continuing execution"
            fi
            ;;
        *)
            if [ -x "${f}" ]; then
                _log "Running executable: ${f}"
                "${f}"
                # shellcheck disable=SC2181
                if [ $? -ne 0 ]; then
                    _log "ERROR: ${f} has failed, continuing execution"
                fi
            else
                _log "Ignoring non-executable: ${f}"
            fi
            ;;
    esac
done
_log "Done running hooks in: ${1}"
