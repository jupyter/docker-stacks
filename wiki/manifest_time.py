# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from pathlib import Path


def get_manifest_timestamp(manifest_file: Path) -> str:
    file_content = manifest_file.read_text()
    TIMESTAMP_PREFIX = "Build timestamp: "
    TIMESTAMP_LENGTH = 20
    timestamp = file_content[
        file_content.find(TIMESTAMP_PREFIX) + len(TIMESTAMP_PREFIX) :
    ][:TIMESTAMP_LENGTH]
    # Should be good enough till year 2100
    assert timestamp.startswith("20"), timestamp
    assert timestamp.endswith("Z"), timestamp
    return timestamp


def get_manifest_year_month(manifest_file: Path) -> str:
    return get_manifest_timestamp(manifest_file)[:7]
