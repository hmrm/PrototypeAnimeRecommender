import numpy as np
import sys
import pca
A = np.matrix(map(lambda x: map(lambda y: float(y), x.split()), sys.stdin.readlines()))
print "Original matrix:"
print A

pca.Center(A)

print "Centered and Scaled matrix:"
print A
p = pca.PCA(A, fraction=0.80)
print "U:"
print p.U
print "d:"
print p.d
print "Vt:"
print p.Vt
print "eigenvalues:"
print p.eigen
print "number of pcs:"
print p.npc
print "udvt:"
print 
