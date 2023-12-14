#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# The run-hooks.sh script looks for *.sh scripts to source
# and executable files to run within a passed directory

if [ "$#" -ne 1 ]; then
    echo "Should pass exactly one directory"
    return 1
fi

if [[ ! -d "${1}" ]]; then
    echo "Directory ${1} doesn't exist or is not a directory"
    return 1
fi

echo "Running hooks in: ${1} as uid: $(id -u) gid: $(id -g)"
for f in "${1}/"*; do
    # Handling a case when the directory is empty
    [ -e "${f}" ] || continue
    case "${f}" in
        *.sh)
            echo "Sourcing shell script: ${f}"
            # shellcheck disable=SC1090
            source "${f}"
            # shellcheck disable=SC2181
            if [ $? -ne 0 ]; then
                echo "${f} has failed, continuing execution"
            fi
            ;;
        *)
            if [ -x "${f}" ]; then
                echo "Running executable: ${f}"
                "${f}"
                # shellcheck disable=SC2181
                if [ $? -ne 0 ]; then
                    echo "${f} has failed, continuing execution"
                fi
            else
                echo "Ignoring non-executable: ${f}"
            fi
            ;;
    esac
done
echo "Done running hooks in: ${1}"
