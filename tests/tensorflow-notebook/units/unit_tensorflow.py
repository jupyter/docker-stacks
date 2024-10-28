# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os

import tensorflow as tf

# Suppress logging warnings
# https://stackoverflow.com/a/78803598
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

print(tf.constant("Hello, TensorFlow"))
print(tf.reduce_sum(tf.random.normal([1000, 1000])))
