#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# The _log function is used for everything these scripts want to log.
# It will always log errors and warnings but can be silenced for other messages
# by setting the JUPYTER_DOCKER_STACKS_QUIET environment variable.
_log () {
    local level="${1}"
    case "${level}" in
        INFO|WARNING|ERROR|DEBUG)
            shift
            ;;
        *)
            level="INFO"
            ;;
    esac
    if [[ "${level}" == "ERROR" ]] || [[ "${level}" == "WARNING" ]] || [[ "${JUPYTER_DOCKER_STACKS_QUIET}" == "" ]]; then
        echo "${level}[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
    fi
}
_log_info () { _log "INFO" "$@"; }
_log_warn () { _log "WARNING" "$@"; }
_log_error () { _log "ERROR" "$@"; }
