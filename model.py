import numpy as np
import scipy.sparse
import sys
from sparsesvd import sparsesvd
np.set_printoptions(threshold=np.nan)

sys.stderr.write("Running Sparse SVD on Data from stdin, Requesting " + sys.argv[1] + " Factors\n")

sys.stderr.write("Reading Data\n")
data = sys.stdin.readlines()
sys.stderr.write("Reformatting Data\n")
data = map((lambda x: x.split()), data)
ilist = []
jlist = []
vlist = []
sys.stderr.write("Populating ijv Lists\n")
for i in xrange(len(data)):
    if not data[i][2] == '0':
        ilist.append(data[i][0])
        jlist.append(data[i][1])
        vlist.append(data[i][2])
sys.stderr.write("Recasting ijv Lists\n")
ilist = map((lambda x: int(x)), ilist)
jlist = map((lambda x: int(x)), jlist)
vlist = map((lambda x: int(x)), vlist)
sys.stderr.write("Recentering and Normalizing ijv Lists\n")
aset = set(jlist)
indexdict = {}
for i in xrange(len(jlist)):
    if jlist[i] in indexdict:
        indexdict[jlist[i]].append(i)
    else:
        indexdict[jlist[i]] = [i]
for a in aset:
    indicies = indexdict[a]
    values = map((lambda x: vlist[x]), indicies)
    stdev = np.std(values)
    avg = sum(values)/len(values)
    for i in indicies:
        vlist[i] -= avg
        if not stdev == 0:
            vlist[i] /= stdev
sys.stderr.write("Creating Sparse Matrix\n")
smat = scipy.sparse.coo_matrix((vlist, (ilist, jlist)))
sys.stderr.write("Transforming Sparse Matrix to csc Format\n")
smat = smat.tocsc()
sys.stderr.write("Running Sparsesvd\n")
ut, s, vt = sparsesvd(smat, int(sys.argv[1]))
sys.stderr.write("Analysis Completed, Printing Data\n")
#print ut
#print s
#print vt
eignum = 0
for eigen in vt:
    eignum += 1
#    print 'in the ' + str(eignum) + '-th archetype:'
    eigpos = np.copy(eigen)
    for i in xrange(10):
        pos = np.argmax(eigpos)
#        print "the " + str(i + 1) + "-th largest positive is: " + str(pos)
        print pos
        eigpos[pos] = 0
    eigneg = np.copy(eigen)
    eigneg *= -1
    for i in xrange(10):
        neg = np.argmax(eigneg)
#        print "the " + str(i + 1) + "-th largest negative is: " + str(neg)
        print neg
        eigneg[neg] = 0
#    print ''
