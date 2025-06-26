#!/usr/local/bin/python
#
#    viterbi.py
#    Viterbi algorithm of HMM for Python.
#    $Id: viterbi.py,v 1.4 2024/08/01 00:12:19 daichi Exp $
#

import sys
import numpy as np
from pylab import *

def viterbi (words, trans, emit):
    T = len(words)
    K,V = emit.shape
    EOS = K
    back = np.zeros ((T,K), dtype=int)
    delta = np.zeros ((T,K), dtype=float)
    # initialize
    t = 0; w = words[t]
    for k in range(K):
        back[t,k] = EOS
        delta[t,k] = emit[k,w] + trans[EOS,k]
    # forward
    for t in range(1,T):
        w = words[t]
        for k in range(K):
            j,lik = vmax (delta[t-1] + trans[0:K,k])
            back[t,k] = j
            delta[t,k] = emit[k,w] + lik
    j,lik = vmax (delta[T-1] + trans[0:K,EOS])
    # backward
    path = []
    for t in reversed(range(T)):
        path.append (j)
        j = back[t,j]
    return list(reversed(path)), lik

def vmax (xx):
    j,val = max (enumerate(xx), key=lambda x: x[1])
    return j,val

def load (file, dicfile):
    # prepare dictionary
    dic = {}
    seed = 0
    with open (dicfile, 'r') as dh:
        for line in dh:
            w = line.rstrip('\n')
            if len(w) > 0:
                dic[w] = seed
                seed += 1
    # load text to integers
    data = []
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            if len(words) > 0:
                sent = [dic[word] for word in words]
                data.append (sent)
    return data

def logmatrix (file):
    X = np.loadtxt (file, dtype=float)
    Y = ma.log (X)
    return Y.filled (-inf)

def usage ():
    print ('usage: % viterbi.py input.txt dict.dat trans.dat emit.dat')
    print ('$Id: viterbi.py,v 1.4 2024/08/01 00:12:19 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        sents = load (sys.argv[1], sys.argv[2])
        trans = logmatrix (sys.argv[3])
        emit  = logmatrix (sys.argv[4])

    for sent in sents:
        states,lik = viterbi (sent, trans, emit)
        print (np.array(states)+1)

if __name__ == "__main__":
    main ()
