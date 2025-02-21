#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import sys

print("Started: b.py")
print(f"OTHER_VAR={os.environ['OTHER_VAR']}")

sys.exit(1)

print("Finished: b.py")
