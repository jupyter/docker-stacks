#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
from pathlib import Path

THIS_DIR = Path(__file__).parent.resolve()


def generate_matrix():
    dockerfiles = sorted(file.name for file in THIS_DIR.glob("*.dockerfile"))
    return {"dockerfile": dockerfiles}


if __name__ == "__main__":
    print("matrix=" + json.dumps(generate_matrix()))
