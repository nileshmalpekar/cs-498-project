#!/usr/bin/env python

import sys
import string

stopWordsPath = sys.argv[1]

stopWords = []
with open(stopWordsPath) as f:
  data = f.read()
  stopWords = data.split()

for line in sys.stdin:
  words = line.strip().lower().split()
  for word in words[2:]:
    if not word in stopWords:
      print '%s\t%s' % (word, 1)
