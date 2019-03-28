#!/usr/bin/env python

import pandas as pd

word_counts_df = pd.read_csv('./public/word-count.txt', sep = '\t', names = ['word', 'count'])
word_counts_df = (word_counts_df.sort_values(['count'], ascending = False).reset_index(drop = True))

for item in word_counts_df.head(100).itertuples(False):
  print "%s\t%s" % (item[1], item[0])
