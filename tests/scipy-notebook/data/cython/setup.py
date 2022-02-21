from setuptools import setup
from Cython.Build import cythonize
from pathlib import Path


THIS_DIR = Path(__file__).parent.resolve()


setup(ext_modules=cythonize(str(THIS_DIR / "helloworld.pyx")))
