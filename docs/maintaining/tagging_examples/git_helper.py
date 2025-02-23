# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from tagging.utils.git_helper import GitHelper

print("Git hash:", GitHelper.commit_hash())
print("Git message:", GitHelper.commit_message())
