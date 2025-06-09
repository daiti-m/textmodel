#!/usr/local/bin/python

import sys
import putil
import numpy as np
from numpy.random import permutation as randperm
from collections import defaultdict
from readword import readword
from eprint import eprintf
from pylab import *

def plot_freqlen (vectors, words, unigram):
    N = len(words)
    xx = []; yy = []
    shown = 0
    # for n in randperm(N):
    for n in range(N):
        word = words[n]
        if not (word in unigram):
            print ('word %s not found in text!' % word)
            continue
        length = veclen(vectors[n,:])
        p = unigram[words[n]]
        xx.append (log(p))
        yy.append (length)
        shown += 1
        if (shown > 20000):
            break
    putil.fontsize (20)
    scatter (xx, yy, c='black')
    xticks (np.arange(-14,0,2))
    xlabel (r'$\log\; p(w)$', fontsize=28, labelpad=6)
    ylabel (r'$|\vec{w}|$', fontsize=28, rotation='horizontal', labelpad=30)

def wordprob (file):
    p = defaultdict (int)
    N = 0
    with open (file, "r") as fh:
        for word in readword(fh):
            p[word] += 1
            N += 1
            if (N % 100000 == 0):
                eprintf("reading words %d..\r" % N)
    eprintf("done.\n")
    for word in p.keys():
        p[word] = p[word] / N
    return p

def veclen (v):
    return np.sqrt (np.dot(v,v))

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

def usage ():
    print ('usage: % vecfreq.py words.vec source.txt [output]')
    print ('$Id: vecfreq.py,v 1.5 2022/07/25 01:40:43 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        wordvec = sys.argv[1]
        text = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else None
    
    vectors, words = loadvec (wordvec)
    unigram = wordprob (text)
    plot_freqlen (vectors, words, unigram)
    if output is not None:
        putil.savefig (output, dpi=200)
    show ()


if __name__ == "__main__":
    main ()
