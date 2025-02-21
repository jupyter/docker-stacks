from tagging.utils.git_helper import GitHelper

print("Git hash:", GitHelper.commit_hash())
print("Git message:", GitHelper.commit_message())
