#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from plumbum.cmd import git


class GitHelper:
    @staticmethod
    def commit_hash() -> str:
        return git["rev-parse", "HEAD"]().strip()  # type: ignore

    @staticmethod
    def commit_hash_tag() -> str:
        return GitHelper.commit_hash()[:12]

    @staticmethod
    def commit_message() -> str:
        return git["log", -1, "--pretty=%B"]().strip()  # type: ignore

    @staticmethod
    def commit_timestamp() -> int:
        return git["log", "-1", "--format=%ct"]().strip()  # type: ignore

    @staticmethod
    def short_commit_hash() -> str:
        return git["rev-parse", "--short", "HEAD"]().strip()  # type: ignore


if __name__ == "__main__":
    print("Git hash:", GitHelper.commit_hash())
    print("Git message:", GitHelper.commit_message())
