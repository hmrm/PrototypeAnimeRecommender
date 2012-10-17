#!/usr/bin/python

import sys
import numpy as np

data = sys.stdin.readlines()
np.random.shuffle(data)
k = int(sys.argv[1])
ssize = len(data) / k
splits = []
for i in xrange(k):
    splits.append(data[i*ssize:(i+1)*ssize])
for i in xrange(k):
    tfile = open(str(i) + '_training', 'w')
    vfile = open(str(i) + '_validation', 'w')
    for j in xrange(k):
        if not i == j:
            for line in splits[j]:
                tfile.write(line)
        else:
            for line in splits[j]:
                vfile.write(line)
