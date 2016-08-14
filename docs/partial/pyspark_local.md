## Using Spark Local Mode

This configuration is nice for using Spark on small, local data.

### In a Python Notebook

0. Run the container as shown above.
1. Open a Python 2 or 3 notebook.
2. Create a `SparkContext` configured for local mode.

For example, the first few cells in the notebook might read:

```python
import pyspark
sc = pyspark.SparkContext('local[*]')

# do something to prove it works
rdd = sc.parallelize(range(1000))
rdd.takeSample(False, 5)
```
