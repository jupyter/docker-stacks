#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import logging
import sys
import time
from pathlib import Path

LOGGER = logging.getLogger(__name__)


def wait_to_finish(tests_results_dir: Path) -> int:
    LOGGER.info("waiting tests to finish")
    # waiting for 5 minutes
    rc_file = tests_results_dir / "rc"
    logs_file = tests_results_dir / "logs"
    error_logs_file = tests_results_dir / "error_logs"
    for attempt in range(300):
        LOGGER.info(f"attempt #{attempt}")
        if rc_file.exists():
            sys.stdout.flush()
            sys.stderr.flush()
            print(logs_file.read_text(), file=sys.stdout)
            sys.stdout.flush()
            print(error_logs_file.read_text(), file=sys.stderr)
            sys.stderr.flush()
            rc = int(rc_file.read_text())
            LOGGER.info(f"rc file was found, rc: {rc}")
            return rc
        time.sleep(1)
    LOGGER.error("tests didn't finish, aborting")
    return 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--tests-results-dir",
        required=True,
        type=Path,
        help="Directory with tests results and return code",
    )
    args = arg_parser.parse_args()

    sys.exit(wait_to_finish(args.tests_results_dir))
