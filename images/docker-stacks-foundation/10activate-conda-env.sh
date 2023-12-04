#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# This registers the initialization code for the conda shell code
# It also activates default environment in the end, so we don't need to activate it manually
# Documentation: https://docs.conda.io/projects/conda/en/latest/dev-guide/deep-dives/activation.html
eval "$(conda shell.bash hook)"
