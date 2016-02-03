#!/usr/bin/env python

import math
import codecs
import os, sys
import time

def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])

def build_entropy_dict(sub_tree, root_gram, finished_nodes):
  result = 0
  for x in sub_tree:
    if x == VALUE_TOKEN: continue
    next_gram = root_gram + x
    finished_nodes = build_entropy_dict(sub_tree[x], next_gram, finished_nodes)
    cnt = sub_tree[x][VALUE_TOKEN]
    pr = cnt/sub_tree[VALUE_TOKEN]
    result += pr * math.log(pr)

  finished_nodes = finished_nodes + 1 if root_gram != '' else finished_nodes
  # skip saving leaf
  if result == 0: return finished_nodes

  time_interval = time.time() - start_time
  if int(time_interval) % 7 == 0:
    sys.stdout.write('\rbuilding entropy dict... {1}/{2} ({3:.2f}%) {0:.1f}s'
        .format(time_interval, finished_nodes, total_nodes, 100.0*finished_nodes/total_nodes))
    sys.stdout.flush()

  # reverse the word back
  if build_type == 'backward': root_gram = root_gram[::-1]
  dict_entropy[root_gram] = -1 * result
  return finished_nodes

def save_entropy_dict(d, file_name):
  f = codecs.open(file_name, 'w', 'utf8')
  for x in d:
    f.write(u'{0}\t{1}\n'.format(x, d[x]))
  f.close()

build_type = ''
if sys.argv[1] == '-f': build_type = 'forward'
elif sys.argv[1] == '-b': build_type = 'backward'
else: raise Exception('please key in -f or -b. E.g., python {0} -b [file_name]'.format(sys.argv[0]))


print '"{0}" entropy'.format(build_type)
print 'input string loading...'

f_input = codecs.open('input_str.utf8', 'r', 'utf8')
input_str = f_input.readlines()[0]
f_input.close()

input_length = len(input_str)
# reverse string for backward
if build_type == 'backward': input_str = input_str[::-1]

grams = []
MAX_GRAM_CNT = 6

total_nodes = 0
VALUE_TOKEN = 'value'
ngram_tree = dict({VALUE_TOKEN: 1.0})

print 'building n-grams...'
for i in range(0, MAX_GRAM_CNT+1):
  start_time = time.time()
  for j, c in enumerate(input_str):
    if j+i >= input_length: break
    d = ngram_tree
    for k in range(j, j+i):
      d = d[input_str[k]]

    t = input_str[j+i]
    if t in d:
      d[t][VALUE_TOKEN] += 1.0
    else:
      d[t] = {VALUE_TOKEN: 1.0}
      total_nodes += 1

  print '{0}-gram DONE {1:.1f}s'.format(i+1, time.time() - start_time)

print '\nbuilding entropy dict...'
start_time = time.time()
dict_entropy = dict()
build_entropy_dict(ngram_tree, '', 0)

print '\nsaving entropy dict...'
file_name = '{0}_entropy_dict.utf8'.format(build_type)
save_entropy_dict(dict_entropy, file_name)
