#!/usr/local/bin/python

import sys
import numpy as np
from usif import uSIF

def cosine (v,w):
    return np.dot(v,w) / (norm(v) * norm(w))

def norm (v):
    return np.sqrt (np.dot (v,v))

def flatten (pairs):
    data = []
    for pair in pairs:
        data.append (pair[0])
        data.append (pair[1])
    return data

def load (file):
    scores = []; pairs = []
    with open (file, 'r') as fh:
        for line in fh:
            data = line.rstrip('\n').split('\t')
            score = float (data[0])
            s1 = data[1].split(' ')
            s2 = data[2].split(' ')
            # accumulate
            scores.append (score)
            pairs.append ((s1,s2))
    return scores, pairs

def usage ():
    print ('ststask: semantic texutual similarity (STS) experiment.')
    print ('usage: % ststask.py sts-test.txt words.vec words.txt')
    print ('$Id: ststask.py,v 1.1 2024/11/08 07:46:07 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        wordvec = sys.argv[2]
        wordtxt = sys.argv[3]

    gold,pairs = load (sys.argv[1])

    embedder = uSIF (wordvec, wordtxt, flatten(pairs))

    N = len(pairs)
    scores = []
    for n in range(N):
        pair = pairs[n]
        score = gold[n]
        # embed!
        v1 = embedder.embed (pair[0])
        v2 = embedder.embed (pair[1])
        s = cosine (v1,v2)
        scores.append (s)
        print ('%f %f' % (gold[n], s))

if __name__ == "__main__":
    main ()
