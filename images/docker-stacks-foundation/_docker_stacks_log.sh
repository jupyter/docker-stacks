#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# The _log function is used for everything these scripts want to log.
# It will always log fatals, errors and warnings but can be silenced for other
# messages by setting the JUPYTER_DOCKER_STACKS_QUIET environment variable.
# Colorizes FATAL, ERROR, WARNING, and DEBUG output when stderr is a terminal.
_log() {
    local level="${1}"
    case "${level}" in
        INFO | WARNING | ERROR | FATAL | DEBUG)
            shift
            ;;
        *)
            level="INFO"
            ;;
    esac
    if [[ "${level}" == "FATAL" ]] || [[ "${level}" == "ERROR" ]] || [[ "${level}" == "WARNING" ]] || [[ "${JUPYTER_DOCKER_STACKS_QUIET}" == "" ]]; then
        local msg
        msg="${level}[$(date '+%Y-%m-%d %H:%M:%S')] $*"
        if [[ -t 2 ]] && [[ "${NO_COLOR:-}" == "" ]]; then
            local color=""
            case "${level}" in
                FATAL) color='1;31' ;; # bold red
                ERROR) color='31' ;;   # red
                WARNING) color='33' ;; # yellow
                DEBUG) color='36' ;;   # cyan
            esac
            if [[ -n "${color}" ]]; then
                msg=$'\033[0;'"${color}m${msg}"$'\033[0m'
            fi
        fi
        echo "${msg}" >&2
    fi
}
_log_info() { _log "INFO" "$@"; }
_log_warn() { _log "WARNING" "$@"; }
_log_error() { _log "ERROR" "$@"; }
_log_fatal() {
    _log "FATAL" "$@"
    exit 1
}
