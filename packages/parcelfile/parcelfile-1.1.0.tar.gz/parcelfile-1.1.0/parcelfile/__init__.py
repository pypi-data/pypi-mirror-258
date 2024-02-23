'''A module used for files, this module was
made to "Package Python Programs Properly". It uses a combination of functions 
perform many file command functions. Creation credits go to @malachi196 on github'''

from zipfile import ZipFile
from .P_Requirments import * #personal module for specific unnamed functions
from .Parcelfile import wrap
from .Parcelfile import box
from .__main__ import STR, INT, ZIPPED, BOOL, FLOAT, MULTI



class colors:
  red = '\033[91m'
  green = '\033[92m'
  yellow = '\033[93m'
  blue = '\033[94m'
  magenta = '\033[95m'
  cyan = '\033[96m'
  white = '\033[97m'
  end = '\033[0m'


__all__ = (
  'ZIPPED',
  'STR',
  'INT',
  'BOOL',
  'FLOAT',
  'MULTI',
  'wrap',
  'box'
)