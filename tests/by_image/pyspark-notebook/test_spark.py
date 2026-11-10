# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)


def test_spark_shell(container: TrackedContainer) -> None:
    """Checking if Spark (spark-shell) is running properly"""
    logs = container.run_and_wait(
        timeout=60,
        no_warnings=False,
        command=["bash", "-c", 'spark-shell <<< "1+1"'],
    )
    warnings = TrackedContainer.get_warnings(logs)
    assert warnings == ["WARNING: Using incubator modules: jdk.incubator.vector"]
    assert "res0: Int = 2" in logs, "spark-shell does not work"


NETTY_CHECK = """
from pyspark.sql import SparkSession

# Spark's RPC and block transfer services are built on Netty
spark = SparkSession.builder.master("local").getOrCreate()
print("sum:", spark.sparkContext.parallelize(range(1000)).sum())

OpenSsl = spark.sparkContext._jvm.io.netty.handler.ssl.OpenSsl
print("OpenSSL available:", OpenSsl.isAvailable(), OpenSsl.unavailabilityCause())
"""


def test_spark_netty(container: TrackedContainer) -> None:
    """Checking if Spark runs on its Netty and netty-tcnative loads"""
    logs = container.run_and_wait(
        timeout=60,
        no_warnings=False,
        command=["python", "-c", NETTY_CHECK],
    )
    warnings = TrackedContainer.get_warnings(logs)
    assert warnings == ["WARNING: Using incubator modules: jdk.incubator.vector"]
    assert "sum: 499500" in logs, "Spark job does not work"
    assert "OpenSSL available: True" in logs, "netty-tcnative doesn't load"
