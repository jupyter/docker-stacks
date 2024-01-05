#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Requirements:
# - Run as the root user

import os
import subprocess
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def get_all_refs(url: str) -> list[str]:
    """
    Get all the references for a given webpage
    """
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)
    return [a["href"] for a in soup.find_all("a", href=True)]


def get_latest_spark_version() -> str:
    """
    Get the last stable version of Spark using spark archive
    """
    all_refs = get_all_refs("https://archive.apache.org/dist/spark/")
    stable_versions = [
        ref.removeprefix("spark-").removesuffix("/")
        for ref in all_refs
        if ref.startswith("spark-") and "incubating" not in ref and "preview" not in ref
    ]
    # We sort versions semantically
    return sorted(
        stable_versions, key=lambda ver: [int(sub_ver) for sub_ver in ver.split(".")]
    )[-1]


def download_spark(spark_version: str, hadoop_version: str) -> None:
    """
    Downloads and unpacks spark
    The resulting spark directory is f"/usr/local/spark-{spark_version}/"
    """
    # You need to use https://archive.apache.org/dist/ website if you want to download old Spark versions
    # But it seems to be slower, that's why we use the recommended site for download
    spark_url = f"https://dlcdn.apache.org/spark/spark-{spark_version}/spark-{spark_version}-bin-hadoop3.tgz"

    tmp_file = Path("/tmp/spark.tar.gz")
    subprocess.check_call(
        ["curl", "--progress-bar", "--location", "--output", tmp_file, spark_url]
    )
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


def prepare_spark(spark_version: str, hadoop_version: str) -> None:
    """
    Creates a SPARK_HOME symlink to a versioned spark directory
    Creates a 10spark-config.sh symlink to source automatically PYTHONPATH
    """
    SPARK_HOME = Path(os.environ["SPARK_HOME"])

    subprocess.check_call(
        [
            "ln",
            "-s",
            f"/usr/local/spark-{spark_version}-bin-hadoop{hadoop_version}",
            SPARK_HOME,
        ]
    )

    # Add a link in the before_notebook hook in order to source automatically PYTHONPATH
    subprocess.check_call(
        [
            "ln",
            "-s",
            f"{SPARK_HOME}/sbin/spark-config.sh",
            "/usr/local/bin/before-notebook.d/10spark-config.sh",
        ]
    )


if __name__ == "__main__":
    HADOOP_VERSION = os.environ["HADOOP_VERSION"]
    spark_version = get_latest_spark_version()
    download_spark(spark_version=spark_version, hadoop_version=HADOOP_VERSION)
    prepare_spark(spark_version=spark_version, hadoop_version=HADOOP_VERSION)
