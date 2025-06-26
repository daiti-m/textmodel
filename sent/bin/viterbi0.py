#!/usr/local/bin/python

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
            delta[t,k] = 
        

    
    w = words[0]
    for k in range(K):
        back[0][k] = EOS
        if (trans[EOS][k] > 0) and (emit[k][w] > 0):
            delta[0][k] = log (emit[k][w]) + log (trans[EOS][k]) 
        else:
            delta[0][k] = -inf
    # forward
    for t in range(1,T):
        w = words[t]
        for k in range(K):
            if emit[k][w] == 0:
                delta[t][k] = -inf
            else:
                j,lik = vmax (k, delta[t-1], trans)
                if j < 0:
                    delta[t][k] = -inf
                else:
                    delta[t][k] = log (emit[k][w]) + lik
                    back[t][k] = j
    # finalize
    j,lik = vmax (EOS, delta[T-1], trans)
    delta[T][EOS] = lik
    back[T][EOS] = j
    print (delta)
    print (back)
    sys.exit (0)
    # backward
    pass

def vmax (k, delta, trans):
    K = len(delta)
    print (delta + log(trans[0:K,k]))
    j,val = max (enumerate (delta + log(trans[0:K,k])), key=lambda x: x[1])
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
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        sents = load (sys.argv[1], sys.argv[2])
        trans = logmatrix (sys.argv[3])
        emit  = logmatrix (sys.argv[4])

#     for sent in sents:
#         states = viterbi (sent, trans, emit)
#         print (sent, states)


if __name__ == "__main__":
    main ()
