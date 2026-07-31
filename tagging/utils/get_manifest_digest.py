# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

import plumbum
from tenacity import (
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_exponential,
)

docker = plumbum.local["docker"]

LOGGER = logging.getLogger(__name__)

MANIFEST_NOT_FOUND_ERRORS = ("manifest unknown", "name unknown", "not found")


class ManifestNotFoundError(RuntimeError):
    """Raised when the registry definitively reports that a manifest doesn't exist"""


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4),
    # A definitive answer from the registry that the manifest doesn't exist
    # is not a transient error, so there is no reason to retry
    retry=retry_if_not_exception_type(ManifestNotFoundError),
)
def get_manifest_digest(tag: str) -> str:
    LOGGER.info(f"Inspecting manifest for tag: {tag}")
    retcode, stdout, stderr = docker[
        "buildx", "imagetools", "inspect", tag, "--format", "{{.Manifest.Digest}}"
    ].run(retcode=None)
    if retcode == 0:
        digest: str = stdout.strip()
        LOGGER.info(f"Manifest for tag: {tag} has digest: {digest}")
        return digest
    output = f"{stdout}\n{stderr}"
    if any(error in output.lower() for error in MANIFEST_NOT_FOUND_ERRORS):
        raise ManifestNotFoundError(
            f"Manifest for tag: {tag} doesn't exist in the registry:\n{output}"
        )
    raise RuntimeError(f"Failed to inspect manifest for tag: {tag}\n{output}")
