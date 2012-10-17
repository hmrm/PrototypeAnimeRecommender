import math
import numpy as np
import scipy.sparse
import sys
from sparsesvd import sparsesvd
np.set_printoptions(threshold=np.nan)

sys.stderr.write("Running Sparse SVD on Data from stdin, Requesting " + sys.argv[1] + " Factors\n")

ilist = []
jlist = []
vlist = []
sys.stderr.write("Populating ijv Lists\n")
line = sys.stdin.readline()
while not line == "":
    line = line.strip().split()
    if not line[2] == '0':
        ilist.append(line[0])
        jlist.append(line[1])
        vlist.append(line[2])
    line = sys.stdin.readline()
sys.stderr.write("Recasting ijv Lists\n")
ilist = map((lambda x: int(x)), ilist)
jlist = map((lambda x: int(x)), jlist)
vlist = map((lambda x: int(x)), vlist)
sys.stderr.write("Recentering and Normalizing ijv Lists\n")
aset = set(jlist)
indexdict = {}
mudict = {}
sigmadict = {}
for i in xrange(len(jlist)):
    if jlist[i] in indexdict:
        indexdict[jlist[i]].append(i)
    else:
        indexdict[jlist[i]] = [i]
for a in aset:
    indicies = indexdict[a]
    values = map((lambda x: vlist[x]), indicies)
    mean = np.mean(values)
    mudict[a] = mean
    stdev = np.std(values)
    sigmadict[a] = stdev
sys.stderr.write("Populating VV ijv Lists\n")
vvfile = open(sys.argv[3], 'r')
line = vvfile.readline()
vilist = []
vjlist = []
vvlist = []
while not line == "":
    line = line.strip().split()
    if not line[2] == '0':
        vilist.append(line[0])
        vjlist.append(line[1])
        vvlist.append(line[2])
    line = vvfile.readline()
sys.stderr.write(str(len(vvlist)) + "\n")
sys.stderr.write("Recasting VV ijv Lists\n")
vilist = map((lambda x: int(x)), vilist)
vjlist = map((lambda x: int(x)), vjlist)
vvlist = map((lambda x: int(x)), vvlist)
sys.stderr.write("Making " + str(len(vvlist)) + " Predictions, Analyzing Performance, and Outputting Errors\n")
for test_no in xrange(len(vvlist)):
    #default prediction
    prediction = 5
    if vjlist[test_no] in aset:
        prediction = mudict[vjlist[test_no]]
    print prediction - vvlist[test_no]
exit()
