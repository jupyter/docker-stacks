#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# This adds NVIDIA Python package libraries to the LD_LIBRARY_PATH.
# Workaround for https://github.com/tensorflow/tensorflow/issues/63362
NVIDIA_DIR=$(dirname "$(python -c 'import nvidia;print(nvidia.__file__)')")
LD_LIBRARY_PATH=$(echo "${NVIDIA_DIR}"/*/lib/ | sed -r 's/\s+/:/g')${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LD_LIBRARY_PATH
