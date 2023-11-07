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
| Month                  |
| ---------------------- |
"""
    wiki_home_file = wiki_dir / "Home.md"
    wiki_home_content = wiki_home_file.read_text()
    month_line = f"| [`{month}`](./{month}) |\n"
    if month_line not in wiki_home_content:
        assert TABLE_BEGINNING in wiki_home_content
        wiki_home_content = wiki_home_content.replace(
            TABLE_BEGINNING, TABLE_BEGINNING + month_line
        )
        wiki_home_file.write_text(wiki_home_content)
        LOGGER.info(f"Updated wiki home page with month: {month}")


def update_monthly_wiki_page(
    wiki_dir: Path, month: str, build_history_line: str
) -> None:
    MONTHLY_PAGE_HEADER = f"""\
# Images built during {month}

| Date | Image | Links |
| - | - | - |
"""
    monthly_page = wiki_dir / "monthly-files" / (month + ".md")
    if not monthly_page.exists():
        monthly_page.write_text(MONTHLY_PAGE_HEADER)
        LOGGER.info(f"Created monthly page: {monthly_page.relative_to(wiki_dir)}")

    monthly_page_content = monthly_page.read_text()
    assert MONTHLY_PAGE_HEADER in monthly_page_content
    monthly_page_content = monthly_page_content.replace(
        MONTHLY_PAGE_HEADER, MONTHLY_PAGE_HEADER + build_history_line + "\n"
    )
    monthly_page.write_text(monthly_page_content)
    LOGGER.info(f"Updated monthly page: {monthly_page.relative_to(wiki_dir)}")


def get_manifest_timestamp(manifest_file: Path) -> str:
    file_content = manifest_file.read_text()
    pos = file_content.find("Build datetime: ")
    return file_content[pos + 16 : pos + 36]


def get_manifest_month(manifest_file: Path) -> str:
    return get_manifest_timestamp(manifest_file)[:7]


def remove_old_manifests(wiki_dir: Path) -> None:
    MAX_NUMBER_OF_MANIFESTS = 4500

    manifest_files: list[tuple[str, Path]] = []
    for file in (wiki_dir / "manifests").rglob("*.md"):
        manifest_files.append((get_manifest_timestamp(file), file))

    manifest_files.sort(reverse=True)
    for _, file in manifest_files[MAX_NUMBER_OF_MANIFESTS:]:
        file.unlink()
        LOGGER.info(f"Removed manifest: {file.relative_to(wiki_dir)}")


def update_wiki(wiki_dir: Path, hist_line_dir: Path, manifest_dir: Path) -> None:
    LOGGER.info("Updating wiki")

    for manifest_file in manifest_dir.glob("*.md"):
        month = get_manifest_month(manifest_file)
        copy_to = wiki_dir / "manifests" / month / manifest_file.name
        copy_to.parent.mkdir(exist_ok=True)
        shutil.copy(manifest_file, copy_to)
        LOGGER.info(f"Added manifest file: {copy_to.relative_to(wiki_dir)}")

    for build_history_line_file in sorted(hist_line_dir.glob("*.txt")):
        build_history_line = build_history_line_file.read_text()
        assert build_history_line.startswith("| `")
        month = build_history_line[3:10]
        update_home_wiki_page(wiki_dir, month)
        update_monthly_wiki_page(wiki_dir, month, build_history_line)

    remove_old_manifests(wiki_dir)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--wiki-dir",
        required=True,
        type=Path,
        help="Directory of the wiki repo",
    )
    arg_parser.add_argument(
        "--hist-line-dir",
        required=True,
        type=Path,
        help="Directory with history lines",
    )
    arg_parser.add_argument(
        "--manifest-dir",
        required=True,
        type=Path,
        help="Directory with manifest files",
    )
    args = arg_parser.parse_args()

    update_wiki(args.wiki_dir, args.hist_line_dir, args.manifest_dir)
