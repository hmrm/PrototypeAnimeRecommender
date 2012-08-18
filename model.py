import numpy as np
import sys
from matplotlib.mlab import PCA

print 'Beginning Analysis'
A = np.array(map(lambda x: map(lambda y: float(y), x.split()[:8]), sys.stdin.readlines()))
print 'Array Loaded'
myPCA = PCA(A)
print 'Principle components'
print myPCA.Wt*myPCA.sigma + myPCA.mu
print 'fracs'
print myPCA.fracs
print 'How To get out of PCA space'
point = myPCA.project([1,2,3,4,5,6,7,8], minfrac=.05)
print point.size
print np.matrix(point - myPCA.mu[:point.size]) * (myPCA.Wt * myPCA.sigma)[:point.size]
