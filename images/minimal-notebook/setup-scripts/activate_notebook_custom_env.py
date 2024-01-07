#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os
import sys
from pathlib import Path

env_name = sys.argv[1]
CONDA_DIR = os.environ["CONDA_DIR"]

file = Path.home() / f".local/share/jupyter/kernels/{env_name}/kernel.json"
content = json.loads(file.read_text())
content["env"] = {
    "XML_CATALOG_FILES": "",
    "PATH": f"{CONDA_DIR}/envs/{env_name}/bin:$PATH",
    "CONDA_PREFIX": f"{CONDA_DIR}/envs/{env_name}",
    "CONDA_PROMPT_MODIFIER": f"({env_name}) ",
    "CONDA_SHLVL": "2",
    "CONDA_DEFAULT_ENV": env_name,
    "CONDA_PREFIX_1": CONDA_DIR,
}

file.write_text(json.dumps(content, indent=1))
