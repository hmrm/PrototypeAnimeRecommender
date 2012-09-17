# remember data -> ijv
import operator
import numpy as np
import scipy.sparse
from scipy.stats import mode
import sys
from sparsesvd import sparsesvd
import scikits.ann as ann
def program():
    np.set_printoptions(threshold=np.nan)
    def getData(infile):
        sys.stderr.write("Reading Data from " + str(infile.name) + "\n")
        i_ = []
        j_ = []
        v_ = []
        line = infile.readline()
        while not line == "":
            line = line.strip().split()
            if not line[2] == "0":
                i_.append(int(line[0]))
                j_.append(int(line[1]))
                v_.append(int(line[2]))
            line = infile.readline()
        sys.stderr.write("Read data, returning lists of length " + str(len(i_)) + "\n")
        return i_, j_, v_
    
    sys.stderr.write("Running Sparse SVD on Data from stdin, Requesting " + sys.argv[1] + " Factors\n")
    def prestuff():
        def normalizeData((i_, j_, v_)):
            sys.stderr.write("Initializing Dictionary\n")
            a_to_indicies = {key : [] for key in set(j_)}
            a_to_u = {key : set([]) for key in set(j_)}
            mudict = {}
            sigmadict = {}
            sys.stderr.write("Writing to Dictionary\n")
            for i in xrange(len(i_)):
                a_to_indicies[j_[i]].append(i)
                a_to_u[j_[i]].add(i_[i])
            sys.stderr.write("Recentering and Normalizing ijv Lists\n")
            for (a, indicies) in a_to_indicies.iteritems():
                values = [v_[x] for x in indicies]
                mean = np.mean(values)
                mudict[a] = mean
                stdev = np.std(values)
                sigmadict[a] = stdev
                for i in indicies:
                    v_[i] -= mean
                    if not stdev == 0:
                        v_[i] /= stdev
            return i_, j_, v_, mudict, sigmadict, a_to_u
        def getSparse(i_, j_, v_):
            sys.stderr.write("Creating Sparse Matrix\n")
            return scipy.sparse.coo_matrix((v_, (i_, j_))).tocsc()
        def doAnalysis(smat):
            sys.stderr.write("Running Sparsesvd\n")
            ut, s, vt = sparsesvd(smat, int(sys.argv[1]))
            return vt
        def getUnsmat(i_, j_, v_):
            ret = {}
            for user in set(i_):
                ret[user] = {}
            for i in xrange(len(i_)):
                ret[i_[i]][j_[i]] = v_[i]
            return ret
        i_, j_, v_ = getData(sys.stdin)
        unsmat = getUnsmat(i_,j_,v_) #un normalized sparse matrix
        i_, j_, v_, m, s, atu = normalizeData((i_, j_, v_))
        smat = getSparse(i_,j_,v_)
        return m, s, doAnalysis(smat), atu, smat, unsmat
    def makePredictions((mu, sigma, vt, a_to_u, smat, unsmat)):
        sys.stderr.write("Analysis Completed, Beginning Making Predictions\n")
        def getvData():
            vtfile = open(sys.argv[2], 'r')
            d_i, d_j, d_v = getData(vtfile)
            return (d_i, d_j, d_v),

        def getProjectedLocs(smat, vt):
            return smat * vt.T

        def actuallyMakePredictions(((d_i, d_j, d_v), vt, mudict, sigmadict, smat, unsmat)):
            sys.stderr.write("Making Predictions")

            min_users = int(sys.argv[3])
            n_recommendations = int(sys.argv[6])

            u_to_index = {key : [] for key in set(d_i)}
            for i in xrange(len(d_i)):
                u_to_index[d_i[i]].append(i)

            for index in u_to_index[0]:
                try: #if data[index][1] in aset:
                    d_v[index] -= mudict[d_j[index]]
                    if not sigmadict[d_j[index]] == 0:
                        d_v[index] /= sigmadict[d_j[index]]
                except KeyError:
                    u_to_index[test_no].remove(index)
            coordinates = []
            for cur_eig in vt:
                coordinates.append(sum(d_v[x]*cur_eig[d_j[x]] for x in u_to_index[0]))
            coordinates = np.array(coordinates)

            plocs = getProjectedLocs(smat, vt) # plocs is a map from users to projected coordinates

            sys.stderr.write("Creating KDTrees\n")
            a_to_kdtree = {}
            a_to_kdtreemap = {}

            a_to_predicted_rating = {}

            for a in a_to_u:
                sys.stderr.write("Estimating Rating for " + str(a) + "\n")
    #default prediction
                prediction = 5
                writeflag = True



                k = int(sys.argv[4])
                rel_users = list(a_to_u[a])
                if len(rel_users) < min_users:
                    sys.stderr.write("Inadequate Data\n")
                    continue
                sys.stderr.write("Found " + str(len(rel_users)) + " Relevant Users\n")
                k = max(1, min(k, len(rel_users) / 2))
                        
                sys.stderr.write("Building KDTree\n")
                a_to_kdtreemap[a] = rel_users
                ploclist = []
                for i in xrange(len(rel_users)):
                    ploclist.append(plocs[rel_users[i]].tolist())
                a_to_kdtree[a] = ann.kdtree(np.array(ploclist))

                knn = a_to_kdtree[a].knn(coordinates, k)[0][0]
                sys.stderr.write("Using K = " + str(k) + "\n")
                knn_ratings = [unsmat[a_to_kdtreemap[a][x]][a] for x in knn]
                mmm = sys.argv[5]
                if mmm == "mean":
                    prediction = np.mean(knn_ratings)
                elif mmm == "median":
                    prediction = np.median(knn_ratings)
                else:
                    prediction = np.argmax(np.bincount(knn_ratings))

                sys.stderr.write("Predicted: " + str(prediction) + "\n")
                a_to_predicted_rating[a] = prediction
            sys.stderr.write("Predictions Complete!\n")
            
            cannot_rec = set([ d_j[index] for index in u_to_index[0] ])

            i = 0
            while i < n_recommendations:
                maxvalue = 0
                maxindex = 0
                for key, value in a_to_predicted_rating.iteritems():
                    if value > maxvalue:
                        maxindex = key
                        maxvalue = value
                top = maxindex
                if not top in cannot_rec:
                    cannot_rec.add(top)
                    print top
                    i += 1
                del a_to_predicted_rating[top]

        actuallyMakePredictions(getvData() + (vt, mu, sigma, smat, unsmat))

    makePredictions(prestuff())

program()        
#cProfile.run("program()")
#sys.stderr.write("Analysis Completed, Printing Data\n")
#print ut.shape
#print s
#for a in s:
#    print a
#exit()
#print vt.shape
#eignum = 0
#for eigen in vt:
#    eignum += 1
#    eigpos = np.copy(eigen)
#    i = 0
#    while i < 10:
#        pos = np.argmax(eigpos)
#        print pos
#        print "the " + str(i + 1) + "-th largest positive is: " + str(pos)
#        if not pos in aucmap:
#            print 4494
#            i += 1
#        elif aucmap[pos] > 900:
#            print pos
#            i += 1
#        i += 1
#        eigpos[pos] = 0
#    eigneg = np.copy(eigen)
#    eigneg *= -1
#    i = 0
#    while i < 10:
#        neg = np.argmax(eigneg)
#        print "the " + str(i + 1) + "-th largest negative is: " + str(neg)
#        if not neg in aucmap:
#            print 4494
#            i += 1
#        elif aucmap[neg] > 900:
#            print neg
#            i += 1
#        print neg
#        i += 1
#        eigneg[neg] = 0
#    print ''
