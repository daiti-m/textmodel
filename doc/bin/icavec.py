#!/usr/local/bin/python
#
#    icavec.py
#    $Id: icavec.py,v 1.2 2023/12/01 11:56:00 daichi Exp $
#
import sys
import numpy as np
from pylab import *
from eprint import eprintf
from scipy.stats import skew
from sklearn.decomposition import FastICA

def ica (X):
    # ICA
    X = X - np.mean (X, axis=0)
    analyzer = FastICA (whiten="arbitrary-variance")
    eprintf ('analyzing ICA.. ')
    S = analyzer.fit_transform (X)
    eprintf ('done.\n')
    # sort by skewness
    N,D = S.shape
    skews = abs (skew (S, axis=0)) # 0=Gaussian
    index = list (map (lambda x: x[1],
                  sorted (zip(skews, arange(D)), key=lambda x: x[0], reverse=True)))
    return S[:,index]

def savevec (file, vectors, words):
    N,D = vectors.shape
    if (N != len(words)):
        print ('error! words do not match.')
        sys.exit (1)
    eprintf ('writing to %s.. ' % file)
    with open (file, 'w') as oh:
        for n in range(N):
            oh.write ('%s\t' % words[n])
            for j in range(D):
                oh.write ('% .7f%s' % (vectors[n][j], ("\n" if j==D-1 else " ")))
    eprintf ('done.\n')
        

def loadvec (file):
    eprintf ('loading from "%s".. ' % file)
    matrix = []
    labels = []
    with open (file, 'r') as fh:
        for line in fh:
            tokens = line.rstrip('\n').split()
            if len(tokens) > 2:
                labels.append (tokens[0])
                matrix.append (list (map (float, tokens[1:])))
                # matrix.append (normalize (list (map (float, tokens[1:]))))
    eprintf ('done.\n')
    return labels, np.array (matrix)

def normalize (v):
    return v / sqrt(np.dot(v, v))

def usage ():
    print ('usage: % icavec.py words.vec output.vec')
    sys.exit (0)

def main ():
    if len(sys.argv) != 3:
        usage ()
    else:
        words,vectors = loadvec (sys.argv[1])
        output  = sys.argv[2]

    icavec = ica (vectors)
    savevec (output, icavec, words)


if __name__ == "__main__":
    main ()
