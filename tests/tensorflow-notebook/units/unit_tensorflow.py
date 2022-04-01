# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import tensorflow as tf

print(tf.constant("Hello, TensorFlow"))
print(tf.reduce_sum(tf.random.normal([1000, 1000])))
