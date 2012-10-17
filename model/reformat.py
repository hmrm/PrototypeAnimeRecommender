import sys

data = sys.stdin.readlines()

for i in xrange(len(data)):
    line = data[i].split(',')
    for pair in line[:len(line) - 1]:
        print str(i) + " " + pair
