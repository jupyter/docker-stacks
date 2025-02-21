#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import plumbum

git = plumbum.local["git"]


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


if __name__ == "__main__":
    print("Git hash:", GitHelper.commit_hash())
    print("Git message:", GitHelper.commit_message())
