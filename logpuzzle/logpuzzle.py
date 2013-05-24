#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  def url_sort_key(url):
    word_pat = re.compile("/.*-\w+-(\w+)\.\w+")
    so = word_pat.search(url)
    if so:
      return so.group(1)
    else:
      return url

  fp = open(filename)
  url_pat = re.compile("_(.*)")
  url_so = url_pat.search(filename)
  url_base = ""
  if url_so:
    url_base = "http://" + url_so.group(1)

  get_pat = re.compile("GET (.*puzzle.*) HTTP")

  img_urls = set()
  for line in fp:
    so = get_pat.search(line)
    if so:
      img_urls.add(url_base + so.group(1))

  fp.close()  
  urls = list(img_urls)  
  return sorted(urls, key = lambda url: url_sort_key(url))
  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  dest = os.path.abspath(dest_dir)
  if not os.path.exists(dest):
    os.makedirs(dest)

  idx_fp = open(dest_dir+"/index.html", "w")
  idx_fp.write('<verbatim><html><body>\n')
  i = 0
  for iu in img_urls:
    img = "img" + str(i)
    dest_img_path = os.path.join(dest, img)

    urllib.urlretrieve(iu, dest_img_path, reporthook = lambda count, block_size, file_size: sys.stdout.write(" Downloading..." + str(count*block_size) + " of " + str(file_size)))
    sys.stdout.write("\n")
    sys.stdout.flush()

    img_tag = '<img src="'+dest_img_path+'" />'
    idx_fp.write(img_tag)
    i += 1
  idx_fp.write('\n</body></html></verbatim>\n')
  idx_fp.close()


def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
