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
    for i in indicies:
        vlist[i] -= mean
        if not stdev == 0:
            vlist[i] /= stdev
sys.stderr.write("Creating Sparse Matrix\n")
smat = scipy.sparse.coo_matrix((vlist, (ilist, jlist)))
sys.stderr.write("Transforming Sparse Matrix to csc Format\n")
smat = smat.tocsc()
sys.stderr.write("Running Sparsesvd\n")
ut, s, vt = sparsesvd(smat, int(sys.argv[1]))
sys.stderr.write("Analysis Completed, Beginning Making Predictions\n")
sys.stderr.write("Reading Validation Data\n")
vtfile = open(sys.argv[2], 'r')
vvfile = open(sys.argv[3], 'r')
ilist = []
jlist = []
vlist = []
sys.stderr.write("Populating VT ijv Lists\n")
line = vtfile.readline()
while not line == "":
    line = line.strip().split()
    if not line[2] == '0':
        ilist.append(line[0])
        jlist.append(line[1])
        vlist.append(line[2])
    line = vtfile.readline()
vilist = []
vjlist = []
vvlist = []
sys.stderr.write("Populating VV ijv Lists\n")
line = vvfile.readline()
while not line == "":
    line = line.strip().split()
    if not line[2] == '0':
        ilist.append(line[0])
        jlist.append(line[1])
        vlist.append(line[2])
    line = vvfile.readline()
#sys.stderr.write("Analysis Completed, Printing Data\n")
#print ut.shape
#print s
#for a in s:
#    print a
#exit()
#print vt.shape
exit()
eignum = 0
for eigen in vt:
    eignum += 1
    eigpos = np.copy(eigen)
    i = 0
    while i < 10:
        pos = np.argmax(eigpos)
        print pos
#        print "the " + str(i + 1) + "-th largest positive is: " + str(pos)
#        if not pos in aucmap:
#            print 4494
#            i += 1
#        elif aucmap[pos] > 900:
#            print pos
#            i += 1
        i += 1
        eigpos[pos] = 0
    eigneg = np.copy(eigen)
    eigneg *= -1
    i = 0
    while i < 10:
        neg = np.argmax(eigneg)
#        print "the " + str(i + 1) + "-th largest negative is: " + str(neg)
#        if not neg in aucmap:
#            print 4494
#            i += 1
#        elif aucmap[neg] > 900:
#            print neg
#            i += 1
        print neg
        i += 1
        eigneg[neg] = 0
#    print ''
