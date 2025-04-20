#!/usr/local/bin/python

import sys
import putil
import numpy as np
from numpy.random import randint
from eprint import eprintf
from pylab import *

def plot_similarities (vectors, N):
    words = list (vectors.keys())
    V = len(words)
    s = np.zeros (N, dtype=float)
    for n in range(N):
        i = randint(V); j = randint(V)
        s[n] = similar (vectors, words[i], words[j])
    hist (s, bins=30, color='black')
    
def similar (vectors, word1, word2):
    if not (word1 in vectors):
        print ("%s is not in vectors!" % word1)
    elif not (word2 in vectors):
        print ("%s is not in vectors!" % word2)
    else:
        return cosine (vectors[word1], vectors[word2])

def cosine (word1, word2):
    return np.dot (word1, word2) / (norm(word1) * norm(word2))

def norm (x):
    return np.sqrt (np.dot(x,x))
        
def vload (file):
    eprintf ('loading from "%s".. ' % file)
    dic = {}
    with open (file, 'r') as fh:
        for line in fh:
            tokens = line.rstrip('\n').split()
            if len(tokens) > 2: # possibly skip word2vec header
                dic[tokens[0]] = np.array (list (map (float, tokens[1:])))
    eprintf ('done.\n')
    return dic

def usage ():
    print ('usage: % similarities.py words.vec N [output]')
    print ('$Id: similarities.py,v 1.3 2022/07/28 09:24:18 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    putil.figsize ((6,3))
    putil.fontsize (20)

    vectors = vload (sys.argv[1])
    N = int (sys.argv[2])
    plot_similarities (vectors, N)
    # axis ([-1,1,0,N/7])
    axis ([-1,1,0,1000])
    xlabel (r'$\cos({\it word}_1,{\it word}_2)$', labelpad=6)
    if len(sys.argv) > 3:
        putil.savefig (sys.argv[3], dpi=200)
    show ()


if __name__ == "__main__":
    main ()
