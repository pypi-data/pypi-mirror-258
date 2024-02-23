'''A module used for files, this module was
made to "Package Python Programs Properly". It uses a combination of functions 
perform many file command functions. Creation credits go to @malachi196 on github'''

import sys as _sys
import os as _os
from zipfile import ZipFile
from .P_Requirments import *
from .__main__ import *

 
class colors:
  red = '\033[91m'
  green = '\033[92m'
  yellow = '\033[93m'
  blue = '\033[94m'
  magenta = '\033[95m'
  cyan = '\033[96m'
  white = '\033[97m'
  end = '\033[0m'

#=====functions=====
def Parcel(*args):
  pass

def measure(filename): # measures length of contents
  with open(filename,'r') as f: 
    fileno = f.fileno()
    print(fileno)

def package(filenames,mode): # packages files
  if mode == mode['zipped'] or ZIPPED:
    modesliteralZIPPED(filepassname=filenames)
    print(f"packaged {filenames}")

def unpackage(filenames): # unpackages files
  print(f"unpackaged {filenames}")
  
def wrap(type,spacing,*args): # wraps (concatinates) items
  results = ""
  try:
    if type == STR: #str
      if spacing == True:
        for arg in args:
          results += arg + " "
        return results
      else:
        for arg in args:
          results += arg 
        return results
    elif type == INT: # int
      if spacing == True:
        for arg in args:
          results += str(arg) + " "
        return results
      else:
        for arg in args:
          results += arg 
        return results
    elif type == BOOL: # bool
      if spacing == True:
        for arg in args:
          results += str(arg).lower() + " "
        return results.lower()
      else:
        for arg in args:
          results += str(arg).lower()
        return results.lower()
    elif type == FLOAT: # float
      if spacing == True:
        for arg in args:
          results += str(arg) + " "
        return results
      else:
        for arg in args:
          results += str(arg)
    elif type == MULTI: # other
      if spacing == True:
        for arg in args:
          results += str(arg).lower() + " "
        return results
      else:
        for arg in args:
          results += str(arg).lower()
        return results
  except Exception as e:
    print(f"An error occoured with process. Exception: {e}")

def box(file,start_line,end_line): # boxes items
  directory = _os.getcwd()
  areaoffi = end_line - start_line
  log = []
  try:
    with open(file, 'r') as f:
      contents = f.read(areaoffi)
      for item in contents:
          log.append('\n'.join(item))
      with open(f"boxed_{file}", "w") as fle:
          fle.write(str(log))
  except OSError as e:
    print(f"error with OS. Exception: {e}")
  except SyntaxError as e:
    print(f"error with givin syntax. Exception: {e}")
  except Exception as e:
    print(f"error with system. Exception: {e}")
