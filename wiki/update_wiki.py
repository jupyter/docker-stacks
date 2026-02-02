#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import datetime
import logging
import shutil
import textwrap
from dataclasses import dataclass
from pathlib import Path

import plumbum
import tabulate
from dateutil import relativedelta

from wiki.config import Config
from wiki.manifest_time import get_manifest_timestamp, get_manifest_year_month

git = plumbum.local["git"]

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


@dataclass
class YearMonthFile:
    month: int
    content: str


@dataclass
class Statistics:
    builds: int
    images: int
    commits: int


def calculate_monthly_stat(
    year_month_file: YearMonthFile, year_month_date: datetime.date
) -> Statistics:
    builds = sum(
        "/base-notebook" in line and "aarch64" not in line
        for line in year_month_file.content.split("\n")
    )

    images = year_month_file.content.count("Build manifest")

    with plumbum.local.env(TZ="UTC"):
        git_log = git[
            "log",
            "--oneline",
            "--since",
            f"{year_month_date}.midnight",
            "--until",
            f"{year_month_date + relativedelta.relativedelta(months=1)}.midnight",
            "--first-parent",
        ]()
    commits = len(git_log.splitlines())
    return Statistics(builds=builds, images=images, commits=commits)


@dataclass
class YearFiles:
    year: int
    files: list[YearMonthFile]


def generate_home_wiki_tables(repository: str, all_years: list[YearFiles]) -> str:
    tables = ""

    GITHUB_COMMITS_URL = (
        f"[{{}}](https://github.com/{repository}/commits/main/?since={{}}&until={{}})"
    )

    YEAR_TABLE_HEADERS = ["Month", "Builds", "Images", "Commits"]

    for year_files in all_years:
        year = year_files.year

        tables += f"\n\n## {year}\n\n"
        year_table_rows = []

        year_stat = Statistics(builds=0, images=0, commits=0)
        for year_month_file in year_files.files:
            month = year_month_file.month
            year_month_date = datetime.date(year=year, month=month, day=1)
            month_stat = calculate_monthly_stat(year_month_file, year_month_date)

            year_stat.builds += month_stat.builds
            year_stat.images += month_stat.images
            year_stat.commits += month_stat.commits

            commits_url = GITHUB_COMMITS_URL.format(
                month_stat.commits,
                year_month_date,
                year_month_date + relativedelta.relativedelta(day=31),
            )
            year_month = f"{year}-{month:0>2}"
            year_table_rows.append(
                [
                    f"[`{year_month}`](./{year_month})",
                    month_stat.builds,
                    month_stat.images,
                    commits_url,
                ]
            )

        year_commits_url = GITHUB_COMMITS_URL.format(
            year_stat.commits, f"{year}-01-01", f"{year}-12-31"
        )
        year_table_rows.append(
            ["**Total**", year_stat.builds, year_stat.images, year_commits_url]
        )

        tables += tabulate.tabulate(
            year_table_rows, YEAR_TABLE_HEADERS, tablefmt="github"
        )
    LOGGER.info("Generated home wiki tables")
    return tables


def write_home_wiki_page(wiki_dir: Path, repository: str) -> None:
    all_years = []
    for year_dir in sorted((wiki_dir / "monthly-files").glob("*"), reverse=True):
        files = sorted(year_dir.glob("*.md"), reverse=True)
        all_years.append(
            YearFiles(
                int(year_dir.name),
                [
                    YearMonthFile(month=int(f.stem[5:]), content=f.read_text())
                    for f in files
                ],
            )
        )
    wiki_home_tables = generate_home_wiki_tables(repository, all_years)

    wiki_home_content = (THIS_DIR / "Home.md").read_text()
    YEAR_MONTHLY_TABLES = "<!-- YEAR_MONTHLY_TABLES -->"

    assert YEAR_MONTHLY_TABLES in wiki_home_content
    wiki_home_content = wiki_home_content[
        : wiki_home_content.find(YEAR_MONTHLY_TABLES) + len(YEAR_MONTHLY_TABLES)
    ]
    wiki_home_content = wiki_home_content.format(REPOSITORY=repository)
    wiki_home_content += wiki_home_tables + "\n"

    (wiki_dir / "Home.md").write_text(wiki_home_content)
    LOGGER.info("Updated Home page")


def update_monthly_wiki_page(wiki_dir: Path, build_history_line: str) -> None:
    assert build_history_line.startswith("| `")
    year_month = build_history_line[3:10]

    MONTHLY_PAGE_HEADER = textwrap.dedent(f"""\
        # Images built during {year_month}

        | Date | Image | Links |
        | - | - | - |
        """)
    year = year_month[:4]
    monthly_page = wiki_dir / "monthly-files" / year / (year_month + ".md")
    if not monthly_page.exists():
        monthly_page.parent.mkdir(parents=True, exist_ok=True)
        monthly_page.write_text(MONTHLY_PAGE_HEADER)
        LOGGER.info(f"Created monthly page: {monthly_page.relative_to(wiki_dir)}")

    monthly_page_content = monthly_page.read_text()
    assert MONTHLY_PAGE_HEADER in monthly_page_content
    monthly_page_content = monthly_page_content.replace(
        MONTHLY_PAGE_HEADER, MONTHLY_PAGE_HEADER + build_history_line + "\n"
    )
    monthly_page.write_text(monthly_page_content)
    LOGGER.info(f"Updated monthly page: {monthly_page.relative_to(wiki_dir)}")


def remove_old_manifests(wiki_dir: Path) -> None:
    MAX_NUMBER_OF_MANIFESTS = 4500

    manifest_files: list[tuple[str, Path]] = []
    for file in (wiki_dir / "manifests").rglob("*.md"):
        manifest_files.append((get_manifest_timestamp(file), file))

    manifest_files.sort(reverse=True)
    for _, file in manifest_files[MAX_NUMBER_OF_MANIFESTS:]:
        file.unlink()
        LOGGER.info(f"Removed manifest: {file.relative_to(wiki_dir)}")


def copy_manifest_files(config: Config) -> None:
    manifest_files = list(config.manifests_dir.rglob("*.md"))
    if not config.allow_no_files:
        assert manifest_files, "expected to have some manifest files"
    for manifest_file in manifest_files:
        year_month = get_manifest_year_month(manifest_file)
        year = year_month[:4]
        copy_to = config.wiki_dir / "manifests" / year / year_month / manifest_file.name
        copy_to.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(manifest_file, copy_to)
        LOGGER.info(f"Added manifest file: {copy_to.relative_to(config.wiki_dir)}")


def update_wiki(config: Config) -> None:
    LOGGER.info("Updating wiki")

    copy_manifest_files(config)

    build_history_line_files = sorted(config.hist_lines_dir.rglob("*.txt"))
    if not config.allow_no_files:
        assert (
            build_history_line_files
        ), "expected to have some build history line files"
    for build_history_line_file in build_history_line_files:
        build_history_line = build_history_line_file.read_text()
        update_monthly_wiki_page(config.wiki_dir, build_history_line)

    write_home_wiki_page(config.wiki_dir, config.repository)
    remove_old_manifests(config.wiki_dir)

    LOGGER.info("Wiki updated")


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
        "--repository",
        required=True,
        help="Repository name on GitHub",
    )
    arg_parser.add_argument(
        "--allow-no-files",
        action="store_true",
        help="Allow no manifest or history line files",
    )
    args = arg_parser.parse_args()

    config = Config(**vars(args))
    update_wiki(config)
