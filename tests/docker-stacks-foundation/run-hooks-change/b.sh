#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

echo "Inside b.sh MY_VAR variable has ${MY_VAR} value"
echo "Changing value of MY_VAR"
export MY_VAR=456
echo "After change inside b.sh MY_VAR variable has ${MY_VAR} value"
