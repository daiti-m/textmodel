#!/usr/local/bin/python
#
#    vwhiten.py
#    $Id: vwhiten.py,v 1.3 2022/07/26 08:50:24 daichi Exp $
#

import sys
import numpy as np
from eprint import eprintf
from readword import readword
from collections import defaultdict
from scipy.linalg import svd
from pylab import *

def whiten (cmatrix, words, unigram):
    # prepare weighted X
    p = []
    for word in words:
        if not (word in words):
            print ('error! word %s not in unigram.' % word)
            sys.exit (0)
        else:
            p.append (unigram[word])
    p = normalize (p)
    norm = sqrt (sum (cmatrix*cmatrix, 1))
    weight = sqrt(p) / norm
    X = weight[:,None] * cmatrix
    # whiten
    eigs,P = eig (np.dot(X.T,X))
    Z = np.dot (X, np.dot(P, diag(1/sqrt(eigs))))
    return Z

def centerize (matrix, words, unigram):
    p = []
    for word in words:
        if not (word in words):
            print ('error! word %s not in unigram.' % word)
            sys.exit (0)
        else:
            p.append (unigram[word])
    p = normalize (p)
    mu = np.dot (p, matrix)
    return matrix - mu

def wordprob (file):
    p = defaultdict (int)
    N = 0
    with open (file, "r") as fh:
        for word in readword(fh):
            p[word] += 1
            N += 1
            if (N % 100000 == 0):
                eprintf("reading from \"%s\" %d words.. \r" % (file, N))
    eprintf("reading from \"%s\" %d words.. done.\n" % (file, N))
    for word in p.keys():
        p[word] = p[word] / N
    return p

def loadvec (file):
    eprintf ('loading from "%s".. ' % file)
    matrix = []; words = []
    with open (file, 'r') as fh:
        for line in fh:
            tokens = line.rstrip('\n').split()
            if len(tokens) > 2: # possibly skip word2vec header
                matrix.append (np.array (list (map (float, tokens[1:]))))
                words.append (tokens[0])
    eprintf ('done.\n')
    return np.array(matrix), words

def save (file, newmatrix, words):
    V,K = newmatrix.shape
    eprintf("writing vectors to %s.. " % file)
    with open (file, "w") as of:
        of.write ("%d %d\n" % (V, K))
        for v in range(V):
            of.write(words[v])
            for k in range(K):
                of.write(" %.8f" % newmatrix[v,k])
            of.write ("\n")
    eprintf("done.\n", clear=False)

def norm (x):
    return np.sqrt (np.dot (x,x))

def normalize (p):
    Z = np.sum(p)
    return p / Z

def usage ():
    print ('usage: % vwhiten.py words.vec text.txt centered.vec')
    print ('$Id: vwhiten.py,v 1.3 2022/07/26 08:50:24 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        wordvec = sys.argv[1]
        text    = sys.argv[2]
        output  = sys.argv[3]

    matrix,words = loadvec (wordvec)
    unigram = wordprob (text)
    eprintf("centerizing..\n")
    cmatrix = centerize (matrix, words, unigram)
    eprintf("rescaling..\n")
    newmatrix = whiten (cmatrix, words, unigram)
    save (output, newmatrix, words)

if __name__ == "__main__":
    main ()
