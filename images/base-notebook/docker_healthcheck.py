#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os
import subprocess
from pathlib import Path

import requests

# Several operations below deliberately don't check for possible errors
# As this is a healthcheck, it should succeed or raise an exception on error

result = subprocess.run(
    ["jupyter", "--runtime-dir"],
    check=True,
    capture_output=True,
    text=True,
    env=dict(os.environ) | {"HOME": str(Path("/home") / os.environ["NB_USER"])},
)
runtime_dir = Path(result.stdout.rstrip())

json_file = next(runtime_dir.glob("*server-*.json"))

url = json.loads(json_file.read_bytes())["url"]
url = url + "api"

proxies = {
    "http": "",
    "https": "",
}

r = requests.get(url, proxies=proxies, verify=False)  # request without SSL verification
r.raise_for_status()
print(r.content)
