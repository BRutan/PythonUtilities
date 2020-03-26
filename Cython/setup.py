from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
import os

setup(
  name='Module Name',
  ext_modules=[Extension('__cythonized_module_name_',
                         ['cythonized_module.pyx'],
                         include_dirs=[numpy.get_include()])],
  # define_macros=[('CYTHON_TRACE', '1')], For enabling profiler.
  cmdclass={'build_ext': build_ext},
)