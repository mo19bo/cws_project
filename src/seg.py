#!/usr/bin/env python

import math
import codecs
import sys
import time

def load_entropy_dict(file_name):
  d = dict()
  f = codecs.open(file_name, 'r', 'utf8')
  for line in f:
    pair = line.rstrip().split('\t')
    d[pair[0]] = float(pair[1])
  return d

print '\ninput string loading...'
f_input = codecs.open('input_str.utf8', 'r', 'utf8')
input_str = f_input.readlines()[0]
f_input.close()

# hyper parameter & data
VAL_DELTA, MAX_GRAM_CNT = float(sys.argv[1]), 6

forward_branch_pos, backward_branch_pos = [], []
input_length = len(input_str)
print 'input length: ' + str(input_length)

start_time = time.time()
print 'loading entropy dict...'
file_name = 'forward_entropy_dict.utf8'
forward_entropy = load_entropy_dict(file_name)

file_name = 'backward_entropy_dict.utf8'
backward_entropy = load_entropy_dict(file_name)
print 'loading entropy dict... {0:.1f} s'.format(time.time() - start_time)

start_time = time.time()
# forward branching
pos_begin, pos_end = 0, 1
entropy_curr, entropy_prev = 0, forward_entropy[input_str[0]]
while pos_end < input_length:
  x = input_str[pos_begin:pos_end]
  entropy_curr = forward_entropy.get(x, 0)
  if entropy_curr - entropy_prev >= VAL_DELTA:
    forward_branch_pos.append(pos_end)
  entropy_prev = entropy_curr
  pos_end += 1
  if pos_end - pos_begin  > MAX_GRAM_CNT:
    begin_limit = forward_branch_pos[-1] - 1 if len(forward_branch_pos) != 0 else pos_begin
    pos_begin = pos_begin + 1 if pos_begin >= begin_limit else begin_limit
    pos_end = pos_begin + 1
    entropy_prev = forward_entropy.get(input_str[pos_begin:pos_end], 0)
    pos_end +=1

sys.stdout.write('\rforward branching... {0:.1f} s \n'.format(time.time() - start_time))
sys.stdout.flush()

start_time = time.time()
# backward branching
pos_begin, pos_end = input_length-1, input_length
entropy_curr, entropy_prev = 0, backward_entropy[input_str[-1]]
while pos_begin > 0:
  x = input_str[pos_begin:pos_end]
  entropy_curr = backward_entropy.get(x, 0)
  if entropy_curr - entropy_prev >= VAL_DELTA:
    backward_branch_pos.append(pos_begin)
  entropy_prev = entropy_curr
  pos_begin -= 1
  if pos_end - pos_begin  > MAX_GRAM_CNT:
    end_limit = backward_branch_pos[-1] + 1 if len(backward_branch_pos) != 0 else pos_end
    pos_end = pos_end - 1 if pos_end <= end_limit else end_limit
    pos_begin = pos_end - 1
    entropy_prev = backward_entropy.get(input_str[pos_begin:pos_end], 0)
    pos_begin -= 1

sys.stdout.write('\rbackward branching... {0:.1f} s \n'.format(time.time() - start_time))
sys.stdout.flush()

start_time = time.time()
print '\ngenerating result...'

branch_pos = {}
branch_pos_set = set(forward_branch_pos) | set(backward_branch_pos)
for pos in branch_pos_set:
  branch_pos[pos] = 0

f_result = codecs.open('seg_result.utf8', 'w', 'utf8')

for idx, s in enumerate(input_str):
  f_result.write(s)
  if idx+1 in branch_pos:
    f_result.write('\n')
    branch_pos.pop(idx+1, None)

f_result.close()
print 'result generation done {0:.1f} s'.format(time.time() - start_time)
