#!/usr/local/bin/python

import sys
import numpy as np
from util import utruncate
from pylab import *

def cosine (x, y):
    return np.dot (x, y)

def mnormalize (X):
    w = sqrt (sum (X*X, 1))
    return dot (diag(1/w), X)

def similars (text, vecs, n, M):
    target = vecs[n]
    scores = np.array ([cosine (target, vec) for vec in vecs])
    shown  = 0
    for sent,score in sorted (zip (text, scores), key=lambda x: x[1], reverse=True):
        print ('% .4f\t%s' % (score, utruncate (sent, 40)))
        shown += 1
        if shown >= M:
            break

def loadtxt (file):
    data = []
    with open (file, 'r') as fh:
        for line in fh:
            sent = line.rstrip('\n').replace(' ', '')
            data.append (sent)
    return data

def loadvec (file):
    return mnormalize (np.loadtxt (file, dtype=float))

def usage ():
    print ('usage: % similars.py sentences.txt sentences.vec n [nshows]')
    print ('n = line number of the sentence to search (begins from 1)')
    print ('$Id: similars.py,v 1.1 2023/04/27 12:40:21 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        text = loadtxt (sys.argv[1])
        vecs = loadvec (sys.argv[2])
        n = int (sys.argv[3]) - 1  # begins from 1
        M = int (sys.argv[4]) if len(sys.argv) > 4 else 15

    similars (text, vecs, n, M)


if __name__ == "__main__":
    main ()
