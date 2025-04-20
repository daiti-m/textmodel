#!/usr/local/bin/python
#
#    bigram.py
#    for Iwanami 'Statistical Text Model' textbook.
#    $Id: bigram.py,v 1.5 2022/07/18 02:13:25 daichi Exp $
#

import sys
import pickle
import numpy as np
from numpy import log,exp
from collections import defaultdict

BOS = '_BOS_'

def parse (file, alpha=0):
    # count occurrences
    freq = {}
    unigram = defaultdict (int)
    with open (file, 'r') as f:
        for line in f:
            s = [c for c in line.rstrip('\n')]
            s.insert (0, BOS)
            s.append (BOS)
            N = len(s)
            for i in range(1,N):
                c = s[i]; h = s[i-1]
                if not (h in freq):
                    freq[h] = defaultdict (int)
                freq[h][c] += 1
                unigram[c] += 1
    # compute conditional probabilities
    p = {}
    V = len(unigram)
    for h in freq:
        Z = sum (freq[h].values())
        p[h] = {}
        for c in freq[h]:
            p[h][c] = (freq[h][c] + alpha) / (Z + V * alpha)
    return { 'p' : p, 'vocab': list(unigram.keys()), 'alpha' : alpha }

def parse_data (text, alpha=0):
    # count occurrences
    freq = {}
    unigram = defaultdict (int)
    for line in text:
        s = [c for c in line.rstrip('\n')]
        s.insert (0, BOS)
        s.append (BOS)
        N = len(s)
        for i in range(1,N):
            c = s[i]; h = s[i-1]
            if not (h in freq):
                freq[h] = defaultdict (int)
            freq[h][c] += 1
            unigram[c] += 1
    # compute conditional probabilities
    p = {}
    V = len(unigram)
    for h in freq:
        Z = sum (freq[h].values())
        p[h] = {}
        for c in freq[h]:
            p[h][c] = (freq[h][c] + alpha) / (Z + V * alpha)
    return { 'p' : p, 'vocab' : list(unigram.keys()), 'alpha' : alpha }

def predict (model, h, c):
    p = model['p']
    vocab = model['vocab']
    # body
    if h in p:
        if c in p[h]:
            return p[h][c]
        else:
            s = sum(p[h].values())
            return (1 - s) / (len(vocab) - len(list(p[h].keys())))
    else:
        sys.stderr.write ('Error! context %s not exist.\n' % h)
        return 0

def predict_file (model, file):
    lik = 0
    with open (file, 'r') as f:
        for line in f:
            s = [c for c in line.rstrip('\n')]
            s.insert (0, BOS)
            s.append (BOS)
            N = len(s)
            for i in range(1,N):
                c = s[i]; h = s[i-1]
                lik += log (predict(model, h, c))
    return lik

def predict_data (model, text):
    lik = 0
    for line in text:
        s = [c for c in line.rstrip('\n')]
        s.insert (0, BOS)
        s.append (BOS)
        N = len(s)
        for i in range(1,N):
            c = s[i]; h = s[i-1]
            lik += log (predict(model, h, c))
    return lik

def usage ():
    print ('usage: % bigram.py file model')
    print ('$Id: bigram.py,v 1.5 2022/07/18 02:13:25 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
        
    model = parse (sys.argv[1], 0.2)
#     with open (sys.argv[1], 'r') as fh:
#         text = fh.readlines()
#     print (predict_data (model, text))
#     print (predict_file (model, sys.argv[1]))
      
    with open (sys.argv[2], 'wb') as out:
        pickle.dump (model, out)

if __name__ == "__main__":
    main ()
