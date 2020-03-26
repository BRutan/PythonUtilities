from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

setup(
  name='Options Monte Carlo',
  ext_modules=[Extension('_optionsmontecarlo_cy',
                         ['options_mc_cython.pyx'],
                         include_dirs=[numpy.get_include()])],
  define_macros=[('CYTHON_TRACE', '1')],
  cmdclass={'build_ext': build_ext},
)