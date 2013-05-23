#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them

def get_special_paths(dir, fileset):
  sps = os.listdir(dir)
  sp_pat = re.compile("__\w+__")
  for sp in sps:
    if sp_pat.search(sp):
      absfilename = os.path.abspath(os.path.join(dir, sp))
      if sp in fileset:
        print "duplicate file", sp, "@", absfilename
      else:
        fileset.add(sp)
        print absfilename
  return fileset

def copy_to(dir, to_dir):
  sp_pat = re.compile("__\w+__")
  sps = filter(lambda sp: sp_pat.search(sp), os.listdir(dir))  

  dest = os.path.abspath(to_dir)
  if not os.path.exists(dest):
    os.makedirs(dest)
  
  for sp in sps:
    src = os.path.abspath(sp)
    shutil.copy(src, os.path.join(dest, sp))

def zip_to(dir, zp):
  sp_pat = re.compile("__\w+__")
  sps = filter(lambda sp: sp_pat.search(sp), os.listdir(dir))

  if os.path.abspath(zp) != zp:
    zp = os.path.abspath(zp)

  zp_dir = os.path.dirname(zp)
  if not os.path.exists(zp_dir):
    os.makedirs(zp_dir)
  
  cmd = 'zip -j ' + zp + ' ' + ' '.join(sps)
  print "command to be run:", cmd
  status, output = commands.getstatusoutput(cmd)
  if status != 0:
    print "zip error: "+output
  else:
    print "done!"


def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  tozip = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]
  elif args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions

  if not todir and not tozip:
    fileset = set()
    for arg in args:
      fileset = get_special_paths(arg, fileset)
  elif todir:
    for arg in args:
      copy_to(arg, todir)
  elif tozip:
    zip_to(args[0], tozip)
  
if __name__ == "__main__":
  main()
