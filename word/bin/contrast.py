#!/usr/local/bin/python

import sys
import numpy as np
from eprint import eprint,eprintf

def contrast (vectors, a, b, x, N):
    scores = []
    words = []
    shown = 0
    target = vectors[x] + (vectors[b] - vectors[a])
    for word,vector in vectors.items():
        scores.append (cosine(vector, target))
        words.append (word)
    for word,score in sorted (zip(words,scores), key=lambda x: x[1], reverse=True):
        if word != x:
            print ('%s -> %.4f' % (word, score))
            shown += 1
        if shown > N:
            break

def cosine (x,y):
    return np.dot(x,y)

def normalize (x):
    return x / np.sqrt (np.dot (x,x))

def jlength (s):
    n = 0
    for c in s:
        if east_asian_width(c) in 'FWA':
            n += 2
        else:
            n += 1
    return n

def vload (file):
    eprintf ('loading from "%s".. ' % file)
    dic = {}
    with open (file, 'r') as fh:
        for line in fh:
            tokens = line.rstrip('\n').split()
            if len(tokens) > 2: # possibly skip word2vec header
                dic[tokens[0]] = normalize (np.array (list (map (float, tokens[1:]))))
    eprintf ('done.\n')
    return dic

def usage ():
    print ('usage: % contrast.py vector.dat word1 word2 word3 [N]')
    print ('$Id: contrast.py,v 1.2 2022/07/23 12:16:31 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 5:
        usage ()
    else:
        vectors = vload (sys.argv[1])
        word1 = sys.argv[2]
        word2 = sys.argv[3]
        word3 = sys.argv[4]
        N = int(sys.argv[5]) if len(sys.argv) > 5 else 20
    
    if not (word1 in vectors):
        print ("'%s' is not in word vectors." % word1)
    elif not (word2 in vectors):
        print ("'%s' is not in word vectors." % word2)
    elif not (word3 in vectors):
        print ("'%s' is not in word vectors." % word3)
    else:
        contrast (vectors, word1, word2, word3, N)

if __name__ == "__main__":
    main ()
