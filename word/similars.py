#!/usr/local/bin/python

import sys
import numpy as np
from eprint import eprint,eprintf
from unicodedata import east_asian_width

def similars (vectors, source, n):
    V = len (vectors)
    target = vectors[source]
    scores = []
    words = []
    shown = 0
    for word,vector in vectors.items():
        scores.append (cosine(target, vector))
        words.append (word)
    for word,score in sorted (zip(words,scores), key=lambda x: x[1], reverse=True):
        if word != source:
            print ('%s -> %.4f' % (word, score))
            # width = max (1, 9 - jlength(word))
            # print ('{}{:{width}s}-> {:.4f}'.format (word, "", score, width=width))
            shown += 1
        if shown > n:
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
    print ('usage: % similars.py vector.dat word [N]')
    print ('$Id: similars.py,v 1.3 2022/07/23 09:59:36 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    vectors = vload (sys.argv[1])
    word = sys.argv[2]
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    if word in vectors:
        similars (vectors, word, n)
    else:
        print ("'%s' is not in word vectors." % word)

if __name__ == "__main__":
    main ()
