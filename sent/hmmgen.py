#!/usr/local/bin/python

import sys
import numpy as np
from numpy.random import rand

def multinom (p):
    s = 0
    K = len(p)
    r = rand()
    for k in range(K):
        s += p[k]
        if (r < s):
            return k
    print ('multinom: error! s = %f' % s)
    return K-1

def gen (trans, emit, dic):
    K,V = emit.shape
    pz = K
    zz = []
    words = []
    while (1):
        z = multinom (trans[pz])
        if (z == K):
            break
        else:
            w = multinom (emit[z])
        zz.append (z+1)
        if dic:
            words.append (dic[w])
        else:
            words.append (w)
        pz = z
    return words, zz

def loaddic (file):
    id = 0
    dic = {}
    with open (file, 'r') as fh:
        for line in fh:
            word = line.rstrip('\n')
            if (word != ""):
                dic[id] = word
                id += 1
    return dic

def usage ():
    print ('usage: hmmgen.py trans.dat emit.dat [dict]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    trans = np.loadtxt (sys.argv[1], dtype=float)
    emit  = np.loadtxt (sys.argv[2], dtype=float)
    dic   = loaddic (sys.argv[3]) if len(sys.argv) > 3 else None

    words, zz = gen (trans, emit, dic)
    print ('words  =', ' '.join(words))
    print ('states =', ' '.join(map(str,zz)))


if __name__ == "__main__":
    main ()
