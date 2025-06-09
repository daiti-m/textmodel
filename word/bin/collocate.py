#!/usr/local/bin/python

import re
import sys
import gzip
import pickle
import numpy as np
from eprint import eprint,eprintf
from collections import defaultdict
from rutil import bernoulli
from pylab import *

def weight (p):
    t = 1e-4  # for medium sized corpus (like text8)
    return max (1 - sqrt(t/p), 0)

def exclude (q, words):
    result = []
    for word in words:
        if word in q:
            if bernoulli (q[word]):
                pass  # exclude
            else:
                result.append (word)
    return result

def parse (file, p, dic, width):
    count = {}
    for word in dic:
        count[word] = defaultdict (int)
    # create filter
    q = {}
    for word in p:
        q[word] = weight (p[word])
    # body
    with open (file, 'r') as fh:
        lines = 0
        for line in fh.readlines():
            if re.match(r'^[ \t\n]*$', line):
                continue
            lines += 1
            if (lines % 1000) == 0:
                eprintf ('processing lines %3d..\r' % lines)
            # count
            # words = line.rstrip('\n').split()
            words = exclude (q, line.rstrip('\n').split())
            T = len (words)
            for t in range(T):
                word = words[t]
                if word in dic:
                    for cword in window (words, t, width):
                        if cword in dic:
                            count[word][cword] += 1
    if (lines >= 1000):
        eprintf ('\n',clear=False)
    return count
    
def window (words, t, width):
    st = t - width
    ed = t + width
    if (st < 0):
        st = 0
    if (ed > len(words) - 1):
        ed = len(words) - 1
    return words[st:t] + words[t+1:ed+1]

def lexicon (file, threshold):
    eprint ('counting lexicon..')
    freq = defaultdict (int)
    lexicon = {}
    p = {}
    seed = 0
    total = 0
    with open (file, 'r') as fh:
        for line in fh.readlines():
            if re.match(r'^[ \t\n]*$', line):
                continue
            words = line.rstrip('\n').split()
            for word in words:
                freq[word] += 1

    for word,count in sorted (freq.items(), key=lambda x: x[1], reverse=True):
        if count >= threshold:
            lexicon[word] = seed
            p[word] = count
            seed += 1
            total += count
    for word in p:
        p[word] = p[word] / total
            
    return lexicon, p

def save (file, counts):
    with gzip.open (file, 'wb') as gf:
        eprintf ('saving to %s..' % file)
        pickle.dump (counts, gf)
    eprint ('done.')

def analyze (file, window, threshold):
    dic,p = lexicon (file, threshold)
    counts = parse (file, p, dic, window)
    return counts

def usage ():
    print ('usage: % collocate.py text model [window] [threshold]')
    print ('$Id: collocate.py,v 1.3 2022/01/05 11:38:38 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        text = sys.argv[1]
        model = sys.argv[2]
        window = int (sys.argv[3]) if len(sys.argv) > 3 else 5
        threshold = int (sys.argv[4]) if len(sys.argv) > 4 else 2
        
    counts = analyze (text, window, threshold)
    save (model, counts)



if __name__ == "__main__":
    main ()
