# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import tensorflow as tf

# These CPU checks must always work, even in the CUDA image running on a host
# without a GPU (importing tensorflow is the whole point of this test)
print(tf.constant("Hello, TensorFlow"))
print(tf.reduce_sum(tf.random.normal([1000, 1000])))

# Only run GPU-specific checks when a GPU is actually available
# (CI runners don't have one, so this block is skipped there)
gpus = tf.config.list_physical_devices("GPU")
if gpus:
    print(f"GPU devices found: {gpus}")
    with tf.device("/GPU:0"):
        print(tf.reduce_sum(tf.random.normal([1000, 1000])))
else:
    print("No GPU found, skipping GPU-specific checks")
