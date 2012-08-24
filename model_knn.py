# remember data -> ijv
import math
import numpy as np
import scipy.sparse
import sys
from sparsesvd import sparsesvd
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
            vvfile = open(sys.argv[3], 'r')
            d_i, d_j, d_v = getData(vtfile)
            sys.stderr.write("Reading Validation Validation Data\n")
            v_i, v_j, v_v = getData(vvfile)
            return (d_i, d_j, d_v), (v_i, v_j, v_v)

        def getProjectedLocs(smat, vt):
            return smat * vt.T

        def actuallyMakePredictions(((d_i, d_j, d_v), (v_i, v_j, v_v), vt, mudict, sigmadict, smat, unsmat)):
            sys.stderr.write("Making " + str(len(v_i)) + " Predictions, Analyzing Performance, and Outputting Errors\n")
            u_to_index = {key : [] for key in set(d_i)}
            for i in xrange(len(d_i)):
                u_to_index[d_i[i]].append(i)
            plocs = getProjectedLocs(smat, vt)
            for test_no in xrange(len(v_v)):
                sys.stderr.write("Executing Test Number " + str(test_no) + " out of " + str(len(v_v)) + "\n")
    #default prediction
                prediction = 5
                try: #if validation[test_no][1] in data:
                    try: #if test_no in u_to_index:
            #normalization and centering
                        for index in u_to_index[test_no]:
                            try: #if data[index][1] in aset:
                                d_v[index] -= mudict[d_j[index]]
                                if not sigmadict[d_j[index]] == 0:
                                    d_v[index] /= sigmadict[d_j[index]]
                            except KeyError:
                                u_to_index[test_no].remove(index)
                        coordinates = []
                        for cur_eig in vt:
                            coordinates.append(sum(d_v[x]*cur_eig[d_j[x]] for x in u_to_index[test_no]))
                        coordinates = np.array(coordinates)
                        k = int(sys.argv[4])
                        rel_users = a_to_u[v_j[test_no]]
                        sys.stderr.write("Found " + str(len(rel_users)) + " Relevant Users\n")
                        k = max(1, min(k, len(rel_users) / 2))
                        knn = []
                        mindist = [k*100] * k #fragile
                        knn = [-1] * k
                        for user in rel_users:
                            d = np.linalg.norm(coordinates - plocs[user])
                            for i in xrange(k):
                                if d < mindist[i]:
                                    mindist.insert(i, d)
                                    mindist.pop()
                                    knn.insert(i, user)
                                    knn.pop()
                                    break
                        knn_ratings = [unsmat[x][v_j[test_no]] for x in knn]
                        mmm = sys.argv[5]
                        if mmm == "mean":
                            prediction = np.mean(knn_ratings)
                        elif mmm == "median":
                            prediction = np.median(knn_ratings)
                        else:
                            prediction = np.mode(knn_ratings)

                    except KeyError:
                        prediction = mudict[v_j[test_no]]
                except KeyError:
                    pass
                print prediction - v_v[test_no]

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
