'''
Emulator is a Python package for constructing emulators.

You can also get documentation for all routines directory from
the interpreter using Python's built-in help() function.
For example:
>>> import BCemu
>>> help(BCemu.use_emul)
'''
import sys
from .download import *
from .simulations import * 

#Suppress warnings from zero-divisions and nans
import numpy
numpy.seterr(all='ignore')
