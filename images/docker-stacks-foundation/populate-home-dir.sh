#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# A mounted home directory shadows the files created in it during the build.
# Restore the files backed up in /opt/default-home to the target home directory,
# never overwriting the files that already exist.
# The restored files are chowned to the owner ("user:group"), if provided.
# Restoring is best-effort: a failure to restore a file only logs a warning,
# because this script is run during startup, which it should never prevent.

set -e

# Source logging functions if not already available
if ! declare -F _log >/dev/null; then
    # shellcheck source=images/docker-stacks-foundation/_docker_stacks_log.sh
    source /usr/local/bin/_docker_stacks_log.sh
fi

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    _log_error "Usage: ${0##*/} <target_home> [<owner>]"
    exit 1
fi

target_home="${1}"
owner="${2:-}"

# A derived image may remove the backup directory to opt out of restoring
if [[ ! -d /opt/default-home ]]; then
    _log_info "Backup directory /opt/default-home doesn't exist, nothing to restore"
    exit 0
fi

# --no-target-directory: merge into a target just created by a concurrent startup
# instead of nesting into it (cp can still lose the race itself)
cp_opts=(--archive --no-target-directory)
if [[ -z "${owner}" ]]; then
    # Running as a non-root user, so don't attempt to preserve the backup files ownership
    cp_opts+=(--no-preserve=ownership)
fi

for backup_entry in /opt/default-home/* /opt/default-home/.*; do
    # The globs expand to the "." and ".." dirs and (if nothing matches) to the pattern itself,
    # neither of which is a real backup entry
    if [[ "${backup_entry}" == */. || "${backup_entry}" == */.. || ! -e "${backup_entry}" ]]; then
        continue
    fi
    target_entry="${target_home}/$(basename "${backup_entry}")"
    if [[ -e "${target_entry}" || -L "${target_entry}" ]]; then
        _log_info "Skipping ${target_entry}, it already exists"
        continue
    fi
    _log_info "Populating missing ${target_entry} from ${backup_entry}"
    if ! cp "${cp_opts[@]}" "${backup_entry}" "${target_entry}"; then
        if [[ -e "${target_entry}" || -L "${target_entry}" ]]; then
            _log_info "Skipping ${target_entry}, it appeared concurrently"
        else
            _log_warn "Failed to populate ${target_entry}"
        fi
    elif [[ -n "${owner}" ]] && ! chown --recursive --no-dereference "${owner}" "${target_entry}"; then
        _log_warn "Failed to change the owner of ${target_entry}"
    fi
done
