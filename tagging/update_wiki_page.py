#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import logging
import shutil
from pathlib import Path

LOGGER = logging.getLogger(__name__)
TABLE_BEGINNING = "|-|-|-|\n"


def update_wiki_page(wiki_dir: Path, hist_line_dir: Path, manifest_dir: Path) -> None:
    LOGGER.info("Updating wiki page")

    wiki_home_file = wiki_dir / "Home.md"
    wiki_home_content = wiki_home_file.read_text()
    build_history_line_files = sorted(hist_line_dir.rglob("*.txt"))
    build_history_lines = "\n".join(
        hist_line_file.read_text() for hist_line_file in build_history_line_files
    )
    wiki_home_content = wiki_home_content.replace(
        TABLE_BEGINNING, TABLE_BEGINNING + build_history_lines + "\n"
    )
    wiki_home_file.write_text(wiki_home_content)
    LOGGER.info("Wiki home file updated")

    for manifest_file in sorted(manifest_dir.rglob("*.md")):
        shutil.copy(manifest_file, wiki_dir / "manifests" / manifest_file.name)
        LOGGER.info(f"Manifest file added: {manifest_file.name}")


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
        "--hist-line-dir",
        required=True,
        type=Path,
        help="Directory to save history line",
    )
    arg_parser.add_argument(
        "--manifest-dir",
        required=True,
        type=Path,
        help="Directory to save manifest file",
    )
    args = arg_parser.parse_args()

    update_wiki_page(args.wiki_dir, args.hist_line_dir, args.manifest_dir)
