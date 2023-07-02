# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from pathlib import Path

from tests.conftest import TrackedContainer

THIS_DIR = Path(__file__).parent.resolve()


def test_cython(container: TrackedContainer) -> None:
    host_data_dir = THIS_DIR / "data/cython"
    cont_data_dir = "/home/jovyan/data"

    logs = container.run_and_wait(
        timeout=10,
        volumes={str(host_data_dir): {"bind": cont_data_dir, "mode": "ro"}},
        tty=True,
        command=[
            "start.sh",
            "bash",
            "-c",
            # We copy our data to temporary folder to be able to modify the directory
            f"cp -r {cont_data_dir}/ /tmp/test/ && cd /tmp/test && python3 setup.py build_ext",
        ],
    )
    assert "building 'helloworld' extension" in logs
