#!/usr/local/bin/python
#
#    phraser.py
#    statistically recognize long phrases with Normalized PMI.
#    $Id: phrase.py,v 1.1 2021/04/29 00:44:47 daichi Exp $
#
import os
import sys
import tempfile
import numpy as np
from collections import defaultdict
from pylab import *

def connect (words, bond):
    N = len (words)
    n = 0
    sentence = []
    while (n < N):
        flag = bond[n]
        if flag == 0:
            sentence.append (words[n])
            n += 1
        else:
            sentence.append (words[n] + '_' + words[n+1])
            n += 2
    return sentence

def collocate (words, phrases):
    N = len(words)
    bond = []
    for n in range(N-1):
        (v,w) = (words[n],words[n+1])
        if (v,w) in phrases:
            bond.append (phrases[(v,w)]) # NPMI > 0
        else:
            bond.append (0)
    bond.append (0)
    # collocate max-first
    while True:
        s = max (bond)
        n = bond.index (s)
        if s == 0:
            break
        # connect maximum
        bond[n] = -1
        if n > 0:
            bond[n-1] = 0
        if n < N-2:
            bond[n+1] = 0
    # join words
    return connect (words, bond)

def parse_write (file, phrases, output):
    with open (file, 'r') as fh:
        with open (output, 'w') as oh:
            for line in fh:
                words = line.rstrip('\n').split()
                if len(words) > 0:
                    sentence = collocate (words, phrases)
                    oh.write (' '.join (sentence) + '\n')
    return output

def compute_phrase (unigram, bigram, threshold=0.5, minfreq=1):
    N = sum (list(unigram.values()))
    phrases = {}
    for bi,freq in bigram.items():
        if freq >= minfreq:
            v = bi[0]; w = bi[1]
            npmi = (log(N) + log(freq) - log(unigram[v]) - log(unigram[w])) \
                    / (log(N) - log(freq))
            if npmi > threshold:
                phrases[bi] = npmi
    return phrases

def count_bigram (file):
    bigram  = defaultdict (int)
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            if len(words) > 0:
                pword = words[0]
                for word in words[1:]:
                    bigram[(pword,word)] += 1
                    pword = word
    return bigram

def count_unigram (file):
    unigram = defaultdict (int)
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            for word in words:
                unigram[word] += 1
    return unigram

def eprint (s,clear=True):
    if clear:
        sys.stderr.write ('\x1b[K')
    sys.stderr.write (s + "\n")
    sys.stderr.flush ()
    
def eprintf (s,clear=True):
    if clear:
        sys.stderr.write ('\x1b[K')
    sys.stderr.write (s)
    sys.stderr.flush ()

def usage ():
    print ('usage: % phrase.py input output passes [threshold] [minfreq]')
    print ('$Id: phrase.py,v 1.1 2021/04/29 00:44:47 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        input  = sys.argv[1]
        output = sys.argv[2]
        iters  = int (sys.argv[3])
        minfreq = int (sys.argv[5]) if len(sys.argv) > 5 else 10
        threshold = float (sys.argv[4]) if len(sys.argv) > 4 else 0.5
        filein = input
    eprint ('computing phrases: threshold = %g minfreq = %d' % (threshold,minfreq))
        
    for iter in range(1,iters+1):
        eprint ('pass [%d/%d]..' % (iter,iters))
        # count n-grams
        eprintf ('- computing phrases..')
        unigram = count_unigram (filein)
        bigram  = count_bigram  (filein)
        phrases = compute_phrase (unigram, bigram, threshold, minfreq)
        # save intermediate file
        if iter == iters:
            fileout = output
        else:
            fileout = tempfile.mktemp()
        eprintf (' writing output..')
        parse_write (filein, phrases, fileout)
        eprintf ('\n')
        if (filein != input):
            os.remove (filein)
        filein = fileout
    eprint ('done.')

if __name__ == "__main__":
    main ()
