#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os
from pathlib import Path

import requests

# A number of operations below deliberately don't check for possible errors
# As this is a healthcheck, it should succeed or raise an exception on error

runtime_dir = Path("/home/") / os.environ["NB_USER"] / ".local/share/jupyter/runtime/"
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
