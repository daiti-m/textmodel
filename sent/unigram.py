#!/usr/local/bin/python

import sys
import numpy as np
from eprint import eprintf
from readword import readword
from collections import defaultdict

def save (p, file):
    with open (file, 'w') as oh:
        for word,prob in sorted (p.items(), key=lambda x: x[1], reverse=True):
            oh.write ('%s\t%e\n' % (word, prob))

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
    print ('usage: % unigram.py text8 text8.p')
    print ('$Id: unigram.py,v 1.1 2022/08/25 20:54:03 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()

    p = unigram (sys.argv[1])
    save (p, sys.argv[2])



if __name__ == "__main__":
    main ()
