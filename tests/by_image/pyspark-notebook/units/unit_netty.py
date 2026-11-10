# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import re
from pathlib import Path

from pyspark.sql import SparkSession

netty_versions = {
    jar.name: re.sub(r".*-(\d+\.\d+\.\d+\.Final).*", r"\1", jar.name)
    for jar in (Path(os.environ["SPARK_HOME"]) / "jars").glob("netty-*.jar")
    if not jar.name.startswith("netty-tcnative")
}
assert netty_versions, "No Netty jars found"
assert len(set(netty_versions.values())) == 1, f"Mixed Netty versions: {netty_versions}"

# Spark's RPC and block transfer services are built on Netty
spark = SparkSession.builder.master("local").getOrCreate()
assert spark.sparkContext.parallelize(range(1000)).sum() == 499500
