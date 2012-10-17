import sys

nms = sys.stdin.readlines()
nms = map(lambda x: float(x), nms)
res = []
for i in xrange( len(nms) - 1):
    res.append(nms[i] / nms[i + 1])
for i in xrange(len(res)):
    print res[i]
