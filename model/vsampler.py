import sys
import numpy as np

tag = sys.argv[1]

dfile = open(tag + "_validation", "r")
vout = open(tag + "_vvalidation", "w")
tout = open(tag + "_tvalidation", "w")
data = dfile.readlines()
for line in data:
    line = line[:-2]
    line = line.split(',')
    line = filter(lambda x: not x[-1] == '0', line)
    if line == []:
        continue
    v = np.random.randint(len(line))
    for i in xrange(len(line)):
        if i == v:
            vout.write(line[i] + ',\n')
        else:
            tout.write(line[i] + ",")
    tout.write('\n')
