#coding=utf8

import codecs
import sys
import time

f_exp = codecs.open(sys.argv[1], 'r', 'utf8') # corpus file name
f_act = codecs.open('seg_result.utf8', 'r', 'utf8')

print 'loading actual result...'
pos_act = set()
list_act = u'　'.join(f_act.readlines()).replace('\n','').replace('\r','').split(u'　')
f_act.close()

print 'loading expected result...'
pos_exp = set()
list_exp = u'　'.join(f_exp.readlines()).replace('\n','').replace('\r','').split(u'　')
f_exp.close()

print 'obtaining sementation position (act)...'
accumulated_pos = 0
for c in list_act:
  accumulated_pos += len(c)
  pos_act.add(accumulated_pos)

print 'obtaining sementation position (exp)...'
accumulated_pos = 0
for c in list_exp:
  accumulated_pos += len(c)
  pos_exp.add(accumulated_pos)

start_time = time.time()
print 'computing score...'
print 'recall = {0:.2f}'.format( float( len(pos_act & pos_exp) ) / len(pos_exp) )
print 'precision = {0:.2f}'.format( float( len(pos_act & pos_exp) ) / len(pos_act) )
