#!/usr/bin/env python
#coding=utf8

import codecs
import sys

print 'build input string...'
fin_name = sys.argv[1]
fin = codecs.open(fin_name, 'r', 'utf8')
fout = codecs.open('input_str.utf8', 'w', 'utf8')

for line in fin:
  line_trim = line.rstrip().replace(u'　', '')
  fout.write(line_trim)

fin.close()
fout.close()
