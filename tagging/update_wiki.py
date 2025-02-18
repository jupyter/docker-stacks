#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import datetime
import logging
import shutil
from pathlib import Path

import plumbum
from dateutil import relativedelta

git = plumbum.local["git"]

LOGGER = logging.getLogger(__name__)


def calculate_monthly_stat(
    year_month_file: Path, year_month_date: datetime.date
) -> tuple[int, int, int]:
    year_month_file_content = year_month_file.read_text()

    builds = sum(
        "jupyter/base-notebook" in line and "aarch64" not in line
        for line in year_month_file_content.split("\n")
    )

    images = year_month_file_content.count("Build manifest")

    with plumbum.local.env(TZ="UTC"):
        future = (
            git[
                "log",
                "--oneline",
                "--since",
                f"{year_month_date}.midnight",
                "--until",
                f"{year_month_date + relativedelta.relativedelta(months=1)}.midnight",
                "--first-parent",
            ]
            & plumbum.BG
        )
    future.wait()
    commits = len(future.stdout.splitlines())

    return builds, images, commits


def regenerate_home_wiki_page(wiki_dir: Path) -> None:
    YEAR_MONTHLY_TABLES = "<!-- YEAR_MONTHLY_TABLES -->\n"

    wiki_home_file = wiki_dir / "Home.md"
    wiki_home_content = wiki_home_file.read_text()

    assert YEAR_MONTHLY_TABLES in wiki_home_content
    wiki_home_content = wiki_home_content[
        : wiki_home_content.find(YEAR_MONTHLY_TABLES) + len(YEAR_MONTHLY_TABLES)
    ]

    YEAR_TABLE_HEADER = """\
## {year}

| Month                  | Builds | Images | Commits                                                                                         |
| ---------------------- | ------ | ------ | ----------------------------------------------------------------------------------------------- |
"""

    GITHUB_COMMITS_URL = (
        "[{}](https://github.com/jupyter/docker-stacks/commits/main/?since={}&until={})"
    )

    for year_dir in sorted((wiki_dir / "monthly-files").glob("*"), reverse=True):
        wiki_home_content += "\n" + YEAR_TABLE_HEADER.format(year=year_dir.name)
        year_builds, year_images, year_commits = 0, 0, 0
        for year_month_file in sorted(year_dir.glob("*.md"), reverse=True):
            year_month = year_month_file.stem
            year_month_date = datetime.date(
                year=int(year_month[:4]), month=int(year_month[5:]), day=1
            )
            builds, images, commits = calculate_monthly_stat(
                year_month_file, year_month_date
            )
            year_builds += builds
            year_images += images
            year_commits += commits
            commits_url = GITHUB_COMMITS_URL.format(
                commits,
                year_month_date,
                year_month_date + relativedelta.relativedelta(day=31),
            )
            monthly_line = f"| [`{year_month}`](./{year_month}) | {builds: <6} | {images: <6} | {commits_url: <95} |\n"
            wiki_home_content += monthly_line
        year_commits_url = GITHUB_COMMITS_URL.format(
            year_commits, f"{year_dir.name}-01-01", f"{year_dir.name}-12-31"
        )
        year_total_line = f"| **Total**              | {year_builds: <6} | {year_images: <6} | {year_commits_url: <95} |\n"
        wiki_home_content += year_total_line

    wiki_home_file.write_text(wiki_home_content)
    LOGGER.info("Updated Home page")


def update_monthly_wiki_page(
    wiki_dir: Path, year_month: str, build_history_line: str
) -> None:
    MONTHLY_PAGE_HEADER = f"""\
# Images built during {year_month}

| Date | Image | Links |
| - | - | - |
"""
    year = year_month[:4]
    monthly_page = wiki_dir / "monthly-files" / year / (year_month + ".md")
    if not monthly_page.exists():
        monthly_page.parent.mkdir(exist_ok=True)
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


def remove_old_manifests(wiki_dir: Path) -> None:
    MAX_NUMBER_OF_MANIFESTS = 4500

    manifest_files: list[tuple[str, Path]] = []
    for file in (wiki_dir / "manifests").rglob("*.md"):
        manifest_files.append((get_manifest_timestamp(file), file))

    manifest_files.sort(reverse=True)
    for _, file in manifest_files[MAX_NUMBER_OF_MANIFESTS:]:
        file.unlink()
        LOGGER.info(f"Removed manifest: {file.relative_to(wiki_dir)}")


def update_wiki(
    *,
    wiki_dir: Path,
    hist_lines_dir: Path,
    manifests_dir: Path,
    allow_no_files: bool,
) -> None:
    LOGGER.info("Updating wiki")

    manifest_files = list(manifests_dir.rglob("*.md"))
    if not allow_no_files:
        assert manifest_files, "expected to have some manifest files"
    for manifest_file in manifest_files:
        year_month = get_manifest_year_month(manifest_file)
        year = year_month[:4]
        copy_to = wiki_dir / "manifests" / year / year_month / manifest_file.name
        copy_to.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(manifest_file, copy_to)
        LOGGER.info(f"Added manifest file: {copy_to.relative_to(wiki_dir)}")

    build_history_line_files = sorted(hist_lines_dir.rglob("*.txt"))
    if not allow_no_files:
        assert (
            build_history_line_files
        ), "expected to have some build history line files"
    for build_history_line_file in build_history_line_files:
        build_history_line = build_history_line_file.read_text()
        assert build_history_line.startswith("| `")
        year_month = build_history_line[3:10]
        update_monthly_wiki_page(wiki_dir, year_month, build_history_line)

    regenerate_home_wiki_page(wiki_dir)
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
        "--hist-lines-dir",
        required=True,
        type=Path,
        help="Directory with history lines",
    )
    arg_parser.add_argument(
        "--manifests-dir",
        required=True,
        type=Path,
        help="Directory with manifest files",
    )
    arg_parser.add_argument(
        "--allow-no-files",
        action="store_true",
        help="Allow no manifest or history line files",
    )
    args = arg_parser.parse_args()

    update_wiki(**vars(args))
