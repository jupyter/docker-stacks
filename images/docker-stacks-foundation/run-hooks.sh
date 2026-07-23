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

# This script might be sourced with errexit enabled (start.sh runs with `set -e`),
# but a failed hook should be logged, not abort the sourcing shell,
# so disable errexit while running hooks and restore it afterwards.
# We intentionally don't run hooks in an errexit-ignoring context (like `if ! source ...`),
# because it would also disable a `set -e` used inside a hook itself,
# and such hooks are expected to fail loudly.
if [[ "$-" == *e* ]]; then
    errexit_was_set="yes"
else
    errexit_was_set="no"
fi
set +e

_log_info "Running hooks in: ${1} as uid: $(id -u) gid: $(id -g)"
for hook_file in "${1}/"*; do
    # Handling a case when the directory is empty
    [ -e "${hook_file}" ] || continue
    case "${hook_file}" in
        *.sh)
            _log_info "Sourcing shell script: ${hook_file}"
            # shellcheck disable=SC1090
            source "${hook_file}"
            hook_rc=$?
            # A sourced hook might have enabled errexit and left it on,
            # so disable it again before running the next hook
            set +e
            if [ "${hook_rc}" -ne 0 ]; then
                _log_error "${hook_file} has failed, continuing execution"
            fi
            ;;
        *)
            if [ -x "${hook_file}" ]; then
                _log_info "Running executable: ${hook_file}"
                "${hook_file}"
                hook_rc=$?
                if [ "${hook_rc}" -ne 0 ]; then
                    _log_error "${hook_file} has failed, continuing execution"
                fi
            else
                _log_info "Ignoring non-executable: ${hook_file}"
            fi
            ;;
    esac
done
_log_info "Done running hooks in: ${1}"

if [[ "${errexit_was_set}" == "yes" ]]; then
    set -e
fi
# This script is sourced, so don't leave the helper variables in the caller's environment
unset errexit_was_set hook_rc hook_file
