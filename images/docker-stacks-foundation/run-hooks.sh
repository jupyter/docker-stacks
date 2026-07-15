#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Source logging functions if not already available
if ! declare -F _log >/dev/null; then
    # shellcheck source=images/docker-stacks-foundation/_docker_stacks_log.sh
    source /usr/local/bin/_docker_stacks_log.sh
fi

# The run-hooks.sh script looks for *.sh scripts to source
# and executable files to run within a passed directory

if [ "$#" -ne 1 ]; then
    _log_error "Should pass exactly one directory"
    return 1
fi

if [[ ! -d "${1}" ]]; then
    _log_error "Directory ${1} doesn't exist or is not a directory"
    return 1
fi

_log_info "Running hooks in: ${1} as uid: $(id -u) gid: $(id -g)"
for f in "${1}/"*; do
    # Handling a case when the directory is empty
    [ -e "${f}" ] || continue
    case "${f}" in
        *.sh)
            _log_info "Sourcing shell script: ${f}"
            # shellcheck disable=SC1090
            source "${f}"
            # shellcheck disable=SC2181
            if [ $? -ne 0 ]; then
                _log_error "${f} has failed, continuing execution"
            fi
            ;;
        *)
            if [ -x "${f}" ]; then
                _log_info "Running executable: ${f}"
                "${f}"
                # shellcheck disable=SC2181
                if [ $? -ne 0 ]; then
                    _log_error "${f} has failed, continuing execution"
                fi
            else
                _log_info "Ignoring non-executable: ${f}"
            fi
            ;;
    esac
done
_log_info "Done running hooks in: ${1}"
