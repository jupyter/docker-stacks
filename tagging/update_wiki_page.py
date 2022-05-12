#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import logging
import shutil
from pathlib import Path


def update_wiki_page(wiki_dir: Path, artifacts_dir: Path) -> None:
    home_wiki_file = wiki_dir / "Home.md"
    file = home_wiki_file.read(home_wiki_file)

    build_history_line_files = artifacts_dir.rglob("**/*.txt")
    build_history_lines = "\n".join(
        hist_line_file.read_text() for hist_line_file in build_history_line_files
    )
    TABLE_BEGINNING = "|-|-|-|\n"
    file = file.replace(TABLE_BEGINNING, TABLE_BEGINNING + build_history_lines + "\n")
    home_wiki_file.write(file)

    for file in artifacts_dir.rglob("**/*.md"):
        shutil.copy(file, wiki_dir / file.name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--wiki-dir",
        required=True,
        type=Path,
        help="Directory for wiki repo",
    )
    arg_parser.add_argument(
        "--artifacts-dir",
        required=True,
        type=Path,
        help="Directory to save history line",
    )
    args = arg_parser.parse_args()

    update_wiki_page(args.wiki_dir, args.artifacts_dir)
