#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Requirements:
# - Run as the root user
# - Required env variable: SPARK_HOME

import argparse
import hashlib
import logging
import os
import re
import subprocess
from pathlib import Path

import requests
from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)


def get_all_refs(url: str) -> list[str]:
    """
    Get all the references for a given webpage
    """
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    return [a["href"] for a in soup.find_all("a", href=True)]


def get_latest_spark_version() -> str:
    """
    Returns the last version of Spark using spark archive
    """
    LOGGER.info("Downloading Spark versions information")
    all_refs = get_all_refs("https://archive.apache.org/dist/spark/")
    LOGGER.info(f"All refs: {all_refs}")
    pattern = re.compile(r"^spark-(\d+\.\d+\.\d+)/$")
    versions = [match.group(1) for ref in all_refs if (match := pattern.match(ref))]
    LOGGER.info(f"Available versions: {versions}")

    # Compare versions semantically
    def version_array(ver: str) -> tuple[int, int, int, str]:
        # 3.5.3 -> [3, 5, 3, ""]
        # 4.0.0-preview2 -> [4, 0, 0, "preview2"]
        arr = ver.split(".")
        assert len(arr) == 3, arr
        major, minor = int(arr[0]), int(arr[1])
        patch, _, preview = arr[2].partition("-")
        return (major, minor, int(patch), preview)

    latest_version = max(versions, key=lambda ver: version_array(ver))
    LOGGER.info(f"Latest version: {latest_version}")
    return latest_version


def get_expected_checksum(spark_version: str, filename: str) -> str:
    """
    Fetches the expected SHA-512 checksum of the Spark tarball
    Current releases live on the download server, old ones only in the archive
    The checksum file contains a line like: `<sha512>  <filename>`
    """
    checksum_urls = [
        f"https://downloads.apache.org/spark/spark-{spark_version}/{filename}.sha512",
        f"https://archive.apache.org/dist/spark/spark-{spark_version}/{filename}.sha512",
    ]
    for checksum_url in checksum_urls:
        LOGGER.info(f"Downloading Spark checksum from: {checksum_url}")
        resp = requests.get(checksum_url, timeout=60)
        if resp.status_code == 404:
            continue
        resp.raise_for_status()
        for token in resp.text.split():
            if re.fullmatch(r"[0-9a-fA-F]{128}", token):
                return token.lower()
        raise RuntimeError(f"No SHA-512 checksum found at: {checksum_url}")
    raise RuntimeError(f"No SHA-512 checksum file found for spark-{spark_version}")


def verify_checksum(tmp_file: Path, expected_checksum: str) -> None:
    """
    Verifies the SHA-512 checksum of the downloaded Spark tarball
    """
    with tmp_file.open("rb") as file:
        actual_checksum = hashlib.file_digest(file, "sha512").hexdigest()
    if actual_checksum != expected_checksum:
        raise RuntimeError(
            f"Spark tarball checksum mismatch: "
            f"expected {expected_checksum}, got {actual_checksum}"
        )
    LOGGER.info("Spark tarball checksum is valid")


def download_spark(
    *,
    spark_version: str,
    hadoop_version: str,
    scala_version: str,
    spark_download_url: Path,
) -> str:
    """
    Downloads, verifies, and unpacks spark
    The resulting spark directory name is returned
    """
    LOGGER.info("Downloading and unpacking Spark")
    spark_dir_name = f"spark-{spark_version}-bin-hadoop{hadoop_version}"
    if scala_version:
        spark_dir_name += f"-scala{scala_version}"
    LOGGER.info(f"Spark directory name: {spark_dir_name}")
    spark_url = spark_download_url / f"spark-{spark_version}" / f"{spark_dir_name}.tgz"
    LOGGER.info(f"Spark download URL: {spark_url}")

    tmp_file = Path("/tmp/spark.tar.gz")
    subprocess.check_call(
        [
            "curl",
            "--progress-bar",
            "--fail",
            "--location",
            "--output",
            tmp_file,
            spark_url,
        ]
    )
    expected_checksum = get_expected_checksum(spark_version, f"{spark_dir_name}.tgz")
    verify_checksum(tmp_file, expected_checksum)
    subprocess.check_call(
        [
            "tar",
            "xzf",
            tmp_file,
            "-C",
            "/usr/local",
            "--owner",
            "root",
            "--group",
            "root",
            "--no-same-owner",
        ]
    )
    tmp_file.unlink()
    return spark_dir_name


def configure_spark(spark_dir_name: str, spark_home: Path) -> None:
    """
    Creates a ${SPARK_HOME} symlink to a versioned spark directory
    Creates a 10spark-config.sh symlink to source PYTHONPATH automatically
    """
    LOGGER.info("Configuring Spark")
    subprocess.check_call(["ln", "-s", f"/usr/local/{spark_dir_name}", spark_home])

    # Add a link in the before_notebook hook in order to source PYTHONPATH automatically
    CONFIG_SCRIPT = "/usr/local/bin/before-notebook.d/10spark-config.sh"
    subprocess.check_call(
        ["ln", "-s", spark_home / "sbin/spark-config.sh", CONFIG_SCRIPT]
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--spark-version", required=True)
    arg_parser.add_argument("--hadoop-version", required=True)
    arg_parser.add_argument("--scala-version", required=True)
    arg_parser.add_argument("--spark-download-url", type=Path, required=True)
    args = arg_parser.parse_args()

    args.spark_version = args.spark_version or get_latest_spark_version()

    spark_dir_name = download_spark(
        spark_version=args.spark_version,
        hadoop_version=args.hadoop_version,
        scala_version=args.scala_version,
        spark_download_url=args.spark_download_url,
    )
    configure_spark(
        spark_dir_name=spark_dir_name, spark_home=Path(os.environ["SPARK_HOME"])
    )
