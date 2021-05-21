#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Set default SoftLayer VM settings
: "${SOFTLAYER_CPU:=4}"
export SOFTLAYER_CPU
: "${SOFTLAYER_DISK_SIZE:=100}"
export SOFTLAYER_DISK_SIZE
: "${SOFTLAYER_MEMORY:=4096}"
export SOFTLAYER_MEMORY
: "${SOFTLAYER_REGION:=wdc01}"
export SOFTLAYER_REGION

docker-machine create --driver softlayer "$@"
