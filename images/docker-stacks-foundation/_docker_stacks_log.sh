#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# The _log function is used for everything these scripts want to log.
# It will always log errors and warnings but can be silenced for other messages
# by setting the JUPYTER_DOCKER_STACKS_QUIET environment variable.
# Colorizes WARNING and ERROR output when stderr is a terminal.
# Respects NO_COLOR (https://no-color.org/).
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
        local msg="${level}[$(date '+%Y-%m-%d %H:%M:%S')] $*"
        if [[ -t 2 ]] && [[ "${NO_COLOR:-}" == "" ]]; then
            local color=""
            case "${level}" in
                ERROR)   color='31' ;;
                WARNING) color='33' ;;
                DEBUG)   color='36' ;;
            esac
            if [[ -n "${color}" ]]; then
                msg=$'\033[0;'"${color}m${msg}"$'\033[0m'
            fi
        fi
        echo "${msg}" >&2
    fi
}
_log_info () { _log "INFO" "$@"; }
_log_warn () { _log "WARNING" "$@"; }
_log_error () { _log "ERROR" "$@"; }
