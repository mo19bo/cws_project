#coding=utf8

import codecs
import sys
import time

f_exp = codecs.open(sys.argv[1], 'r', 'utf8') # corpus file name
f_act = codecs.open('seg_result.utf8', 'r', 'utf8')

print 'loading actual result...'
pos_act = set()
str_act = ''
str_act = u'　'.join(f_act.readlines()).replace('\n','').replace('\r','')
f_act.close()

print 'loading expected result...'
pos_exp = set()
str_exp = u'　'.join(f_exp.readlines()).replace('\n','').replace('\r','')
f_exp.close()

print 'obtaining sementation position (act)...'
for idx, c in enumerate(str_act):
  if c == u'　': pos_act.add(idx)

print 'obtaining sementation position (exp)...'
for idx, c in enumerate(str_exp):
  if c == u'　': pos_exp.add(idx)

start_time = time.time()
print 'computing score...'
print 'recall = {0:.2f}'.format( float( len(pos_act & pos_exp) ) / len(pos_exp) )
print 'presision = {0:.2f}'.format( float( len(pos_act & pos_exp) ) / len(pos_act) )
