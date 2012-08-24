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
            mudict = {}
            sigmadict = {}
            sys.stderr.write("Writing to Dictionary\n")
            for i in xrange(len(i_)):
                a_to_indicies[j_[i]].append(i)
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
            return i_, j_, v_, mudict, sigmadict
        def getSparse(i_, j_, v_):
            sys.stderr.write("Creating Sparse Matrix\n")
            return scipy.sparse.coo_matrix((v_, (i_, j_))).tocsc()
        def doAnalysis(smat):
            sys.stderr.write("Running Sparsesvd\n")
            ut, s, vt = sparsesvd(smat, int(sys.argv[1]))
            return vt

        i_, j_, v_, m, s = normalizeData(getData(sys.stdin))
        return m, s, doAnalysis(getSparse(i_, j_, v_))
    def makePredictions((mu, sigma, vt)):
        sys.stderr.write("Analysis Completed, Beginning Making Predictions\n")
        def getvData():
            vtfile = open(sys.argv[2], 'r')
            vvfile = open(sys.argv[3], 'r')
            d_i, d_j, d_v = getData(vtfile)
            sys.stderr.write("Reading Validation Validation Data\n")
            v_i, v_j, v_v = getData(vvfile)
            return (d_i, d_j, d_v), (v_i, v_j, v_v)
        def actuallyMakePredictions(((d_i, d_j, d_v), (v_i, v_j, v_v), vt, mudict, sigmadict)):
            sys.stderr.write("Making " + str(len(v_i)) + " Predictions, Analyzing Performance, and Outputting Errors\n")
            u_to_index = {key : [] for key in set(d_i)}
            for i in xrange(len(d_i)):
                u_to_index[d_i[i]].append(i)

            for test_no in xrange(len(v_v)):
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
                        prediction_direction = vt[0] - vt[0]
                        for cur_eig in vt:
                            prediction_direction += cur_eig * sum(d_v[x]*cur_eig[d_j[x]] for x in u_to_index[test_no])
                            
                        
                        #for cur_eig in vt:
                        #    coefficient = sum(data[x][2]*cur_eig[data[x][1]] for x in u_to_index[test_no]) 
                        #    prediction_direction += coefficient*cur_eig
                        prediction = prediction_direction[v_j[test_no]] * sigmadict[v_j[test_no]] + mudict[v_j[test_no]]
                    except KeyError:
                        prediction = mudict[v_j[test_no]]
                except KeyError:
                    pass
                print prediction - v_v[test_no]

        actuallyMakePredictions(getvData() + (vt, mu, sigma))

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
