# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging


LOGGER = logging.getLogger(__name__)


def test_spark_shell(container):
    """Checking if Spark (spark-shell) is running properly"""
    c = container.run(
        tty=True,
        command=["start.sh", "bash", "-c", 'spark-shell <<< "1+1"'],
    )
    c.wait(timeout=60)
    logs = c.logs(stdout=True).decode("utf-8")
    LOGGER.debug(logs)
    assert "res0: Int = 2" in logs, "spark-shell does not work"
