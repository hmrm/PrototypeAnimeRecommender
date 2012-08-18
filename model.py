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
sys.stderr.write("Recentering ijv Lists\n")
aset = set(jlist)
for a in aset:
    indicies = filter((lambda x: jlist[x] == a), range(len(jlist)))
    values = map((lambda x: vlist[x]), indicies)
    avg = sum(values)/len(values)
    for i in indicies:
        vlist[i] -= avg
sys.stderr.write("Creating Sparse Matrix\n")
smat = scipy.sparse.coo_matrix((vlist, (ilist, jlist)))
sys.stderr.write("Transforming Sparse Matrix to csc Format\n")
smat = smat.tocsc()
sys.stderr.write("Running Sparsesvd\n")
ut, s, vt = sparsesvd(smat, int(sys.argv[1]))
sys.stderr.write("Analysis Completed, Printing Data\n")
print ut
print s
print vt
