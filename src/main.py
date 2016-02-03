#!/usr/bin/env python

import subprocess as sp
import sys

corpus_file_name = sys.argv[1]
VAL_DELTA = sys.argv[2]

sp.call('python build_input.py {0}'.format(corpus_file_name), shell=True)
sp.call('python build_entropy_dict.py -f', shell=True)
sp.call('python build_entropy_dict.py -b', shell=True )
sp.call('python seg.py {0}'.format(VAL_DELTA), shell=True)
sp.call('python compute_score.py {0}'.format(corpus_file_name), shell=True)
