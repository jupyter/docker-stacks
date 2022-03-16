# These lines are not sorted by isort on purpose
# see: https://stackoverflow.com/a/53356077/4881441
from setuptools import setup  # isort:skip
from Cython.Build import cythonize  # isort:skip

setup(ext_modules=cythonize("helloworld.pyx"))
