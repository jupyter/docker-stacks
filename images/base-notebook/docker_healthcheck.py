#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os
import subprocess
import sys
from pathlib import Path

import requests

# Several operations below deliberately don't check for possible errors
# As this is a health check, it should succeed or raise an exception on error

# Docker runs health checks using an exec
# It uses the default user configured when running the image: root for the case of a custom NB_USER or jovyan for the case of the default image user.
# We manually change HOME to make `jupyter --runtime-dir` report a correct path
# More information: <https://github.com/jupyter/docker-stacks/pull/2074#issuecomment-1879778409>
result = subprocess.run(
    ["jupyter", "--runtime-dir"],
    check=True,
    capture_output=True,
    text=True,
    env=dict(os.environ) | {"HOME": "/home/" + os.environ["NB_USER"]},
)
runtime_dir = Path(result.stdout.rstrip())

json_file = next(runtime_dir.glob("*server-*.json"))

url = json.loads(json_file.read_bytes())["url"]

# The server might not be listening on HTTP(S), for example,
# when it only listens on a UNIX socket (`c.ServerApp.sock` is configured).
# In this case, there is no TCP URL we can check, so report a healthy state.
if not url.startswith(("http://", "https://")):
    print(f"Skipping the check for the non-HTTP(S) server URL: {url}")
    sys.exit(0)

url = url + "api"

proxies = {
    "http": "",
    "https": "",
}

r = requests.get(url, proxies=proxies, verify=False)  # request without SSL verification
r.raise_for_status()
print(r.content)
