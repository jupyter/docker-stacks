#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import logging
import shutil
from pathlib import Path

LOGGER = logging.getLogger(__name__)


def update_home_wiki_page(wiki_dir: Path, month: str) -> None:
    TABLE_BEGINNING = """\
| Month |
| - |
"""
    wiki_home_file = wiki_dir / "Home.md"
    wiki_home_content = wiki_home_file.read_text()
    month_line = f"| `{month}` | [`link`](./{month}) |\n"
    if month_line not in wiki_home_content:
        wiki_home_content = wiki_home_content.replace(
            TABLE_BEGINNING, TABLE_BEGINNING + month_line
        )
        wiki_home_file.write_text(wiki_home_content)
        LOGGER.info(f"Wiki home file updated with month: {month}")


def update_monthly_wiki_page(
    wiki_dir: Path, month: str, build_history_line: str
) -> None:
    MONTHLY_PAGE_HEADER = f"""\
# Images built during {month}

| Date | Image | Links |
| - | - | - |
"""
    monthly_page = wiki_dir / (month + ".md")
    if not monthly_page.exists():
        monthly_page.write_text(MONTHLY_PAGE_HEADER)
        LOGGER.info(f"Created monthly page: {month}")

    monthly_page_content = monthly_page.read_text().replace(
        MONTHLY_PAGE_HEADER, MONTHLY_PAGE_HEADER + build_history_line + "\n"
    )
    monthly_page.write_text(monthly_page_content)


def update_wiki(wiki_dir: Path, hist_line_dir: Path, manifest_dir: Path) -> None:
    LOGGER.info("Updating wiki")

    LOGGER.info("Copying manifest files")
    for manifest_file in manifest_dir.glob("*.md"):
        shutil.copy(manifest_file, wiki_dir / "manifests" / manifest_file.name)
        LOGGER.info(f"Manifest file added: {manifest_file.name}")

    for build_history_line_file in sorted(hist_line_dir.glob("*.txt")):
        build_history_line = build_history_line_file.read_text()
        assert build_history_line.startswith("| `")
        month = build_history_line[3:10]
        update_home_wiki_page(wiki_dir, month)
        update_monthly_wiki_page(wiki_dir, month, build_history_line)


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

    update_wiki(args.wiki_dir, args.hist_line_dir, args.manifest_dir)
