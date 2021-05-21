#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Set reasonable default VM settings
: "${VIRTUALBOX_CPUS:=4}"
export VIRTUALBOX_CPUS
: "${VIRTUALBOX_MEMORY_SIZE:=4096}"
export VIRTUALBOX_MEMORY_SIZE

docker-machine create --driver virtualbox "$@"
