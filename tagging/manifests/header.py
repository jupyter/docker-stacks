# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import plumbum

from tagging.utils.config import Config
from tagging.utils.git_helper import GitHelper

docker = plumbum.local["docker"]


class ManifestHeader:
    """ManifestHeader doesn't fall under common interface, and we run it separately"""

    @staticmethod
    def create_header(
        config: Config,
        build_timestamp: str,
    ) -> str:
        commit_hash = GitHelper.commit_hash()
        commit_hash_tag = GitHelper.commit_hash_tag()
        commit_message = GitHelper.commit_message()

        # Unfortunately, `docker images` doesn't work when specifying `docker.io` as registry
        fixed_registry = config.registry + "/" if config.registry != "docker.io" else ""

        image_size = docker[
            "images",
            f"{fixed_registry}{config.owner}/{config.image}:latest",
            "--format",
            "{{.Size}}",
        ]().rstrip()

        return f"""\
# Build manifest for image: {config.image}:{commit_hash_tag}

## Build Info

- Build timestamp: {build_timestamp}
- Docker image: `{config.full_image()}:{commit_hash_tag}`
- Docker image size: {image_size}
- Git commit SHA: [{commit_hash}](https://github.com/{config.repository}/commit/{commit_hash})
- Git commit message:

```text
{commit_message}
```"""
