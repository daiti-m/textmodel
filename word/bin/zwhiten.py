#!/usr/local/bin/python
#
#    vwhiten.py
#    $Id: zwhiten.py,v 1.6 2024/11/29 03:48:54 daichi Exp $
#
import re
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
    X = np.dot (diag(p), cmatrix)
    # whiten
    eigs,P = eig (np.dot(X.T,X))
    Z = np.dot (X, np.dot(P, diag(1/sqrt(eigs))))
    return Z

def centerize (matrix, words, unigram):
    p = []
    newwords = []
    newmatrix = []
    V = matrix.shape[0]
    for v in range(V):
        word = words[v]
        if (word in unigram):
            p.append (unigram[word])
            newwords.append (word)
            newmatrix.append (matrix[v])
    p = normalize (p)
    mu = np.dot (p, newmatrix)
    return newmatrix - mu, newwords

def wordprob (file):
    if re.search (r'\.p$', file):
        return loadp (file)
    else:
        return unigram (file)

def loadp (file):
    eprintf ('loading word probabilities from "%s".. ' % file)
    p = {}
    with open (file, 'r') as fh:
        for line in fh:
            tokens = line.rstrip('\n').split('\t')
            if not (len(tokens) == 2):
                print ('error! invalid line.')
                sys.exit (1)
            else:
                word = tokens[0]
                prob = float (tokens[1])
                p[word] = prob
    eprintf ('done.\n', clear=False)
    return p

def unigram (file):
    freq = defaultdict (int)
    p = {}
    N = 0
    with open (file, "r") as fh:
        for word in readword(fh):
            freq[word] += 1
            N += 1
            if (N % 100000 == 0):
                eprintf ("reading from \"%s\" %s words.. \r" % (file, N))
    eprintf ("reading from \"%s\" %s words.. done.\n" % (file, N))
    for word in freq.keys():
        p[word] = freq[word] / N
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
    print ('usage: % vwhiten.py words.vec text.{txt,p} centered.vec')
    print ('$Id: zwhiten.py,v 1.6 2024/11/29 03:48:54 daichi Exp $')
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
    eprintf("centering..\n")
    cmatrix,newwords = centerize (matrix, words, unigram)
    eprintf("whitening..\n")
    newmatrix = whiten (cmatrix, newwords, unigram)
    save (output, newmatrix, newwords)

if __name__ == "__main__":
    main ()
