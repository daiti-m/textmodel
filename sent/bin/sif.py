#!/usr/local/bin/python
#
#    SIF.py
#    smoothed inverse frequency sentence embedding.
#    $Id: sif.py,v 1.1 2024/07/25 04:35:06 daichi Exp $
#

import sys
import numpy as np
from eprint import eprintf
from readword import readword
from collections import defaultdict
from pylab import *

def sif (p,a):
    return a / (p + a)

def embed (sent, wordvec, wordp, a=1e-4):
    vectors = []
    for word in sent:
        if (word in wordvec) and (word in wordp):
            p = wordp[word]
            vec = wordvec[word]
            vectors.append (sif (p, a) * vec)
    return np.mean (vectors, axis=0)

def loadtxt (file):
    data = []
    with open (file, 'r') as fh:
        for line in fh:
            sent = line.rstrip('\n').split()
            data.append (sent)
    return data
    
def loadvec (file):
    eprintf ('loading from "%s".. ' % file)
    vectors = {}
    with open (file, 'r') as fh:
        for line in fh:
            tokens = line.rstrip('\n').split()
            if len(tokens) > 2: # possibly skip word2vec header
                word = tokens[0]
                vectors[word] = np.array (list (map (float, tokens[1:])))
    eprintf ('done.\n')
    return vectors

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
            if (N % 1000000 == 0):
                eprintf ("reading from \"%s\" %s words.. \r" % (file, N))
    eprintf ("reading from \"%s\" %s words.. done.\n" % (file, N))
    for word in freq.keys():
        p[word] = freq[word] / N
    return p

def usage ():
    print ('usage: % sif.py wordvec.vec corpus.txt sent.txt')
    print ('$Id: sif.py,v 1.1 2024/07/25 04:35:06 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        wordvec = loadvec (sys.argv[1])
        wordp = wordprob (sys.argv[2])
        sents = loadtxt (sys.argv[3])

    for sent in sents:
        v = embed (sent, wordvec, wordp, 1e-4)
        print (sent)
        print (v)
    
            
if __name__ == "__main__":
    main ()
