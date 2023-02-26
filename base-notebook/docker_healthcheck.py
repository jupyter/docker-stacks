import json
import os

import requests

# A number of operations below delibrately don't check for possible errors
# As this is a healthcheck, it should succeed or raise an exception on error

runtime_dir = "/home/" + os.environ["NB_USER"] + "/.local/share/jupyter/runtime/"
file_list = os.listdir(runtime_dir)
json_file = [s for s in file_list if s.endswith(".json")]

url = json.load(open(runtime_dir + json_file[0]))["url"]
url = url + "api"

r = requests.get(url, verify=False)  # request without SSL verification
r.raise_for_status()
print(r.content)
