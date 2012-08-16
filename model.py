import numpy as np
import sys
matrix = np.matrix( map(lambda x: map(lambda y: float(y), x.split()), sys.stdin.readlines()) )
print "Original matrix:"
print matrix
U, s, V = np.linalg.svd( matrix )
print "U:"
print U
print "sigma:"
print s
print "VT:"
print V
dimensions = 1
rows,cols = np.matrix.shape
#Dimension reduction, build SIGMA'
for index in xrange(dimensions, rows):
 s[index]=0
print "reduced sigma:"
print s
#Reconstruct MATRIX'
reconstructedMatrix= np.dot(np.dot(U,np.linalg.diagsvd(s,len(matrix),len(V))),V)
#Print transform
print "reconstructed:"
print reconstructedMatrix