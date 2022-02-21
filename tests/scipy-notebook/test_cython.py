# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging
from pathlib import Path
import shutil
import tempfile

from conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


def test_cython(container: TrackedContainer) -> None:
    data_dir = THIS_DIR / "data/cython"

    with tempfile.TemporaryDirectory() as host_data_dir:
        """We create temporary dir with the same content to mount it as a writeable folder
        This allows to run this test in parallel many times
        """
        shutil.copy(data_dir / "helloworld.pyx", host_data_dir)
        shutil.copy(data_dir / "setup.py", host_data_dir)

        cont_data_dir = "/home/jovyan/data"
        command = "sleep infinity"

        running_container = container.run_detached(
            volumes={str(host_data_dir): {"bind": cont_data_dir, "mode": "rw"}},
            tty=True,
            command=["start.sh", "bash", "-c", command],
        )
        command = f"python {cont_data_dir}/setup.py build_ext --inplace"
        cmd = running_container.exec_run(command)
        LOGGER.debug(cmd.output.decode("utf-8"))
        assert cmd.exit_code == 0, f"Command {command} failed"
