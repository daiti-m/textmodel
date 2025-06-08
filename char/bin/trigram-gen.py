#!/usr/local/bin/python
#
#    trigram-gen.py
#    generation from trigram distributions.
#    $Id: trigram-gen.py,v 1.1 2020/11/11 00:26:29 daichi Exp $
#
import sys
import pickle
import numpy as np
from collections import defaultdict
from numpy.random import rand, randint

BOS = '_BOS_'

def randchar (p):
    s = 0
    r = rand()
    for c in p:
        s += p[c]
        if (r < s):
            return c
    return c

def gen_char (dic, dic1, h):
    if not (h in dic):
        return randchar (dic1)
    else:
        s = 0
        r = rand()
        for (c,p) in dic[h].items():
            s += p
            if (r < s):
                return c
        return c

def gen (model, model1):
    s = ''
    h1 = BOS
    h2 = BOS
    while True:
        h = h2 + '|' + h1
        c = gen_char (model, model1, h)
        if (c == BOS):
            return s
        else:
            s += c
            h2 = h1
            h1 = c

def unigram (model):
    p = defaultdict (float)
    Z = 0
    for h in model:
        for c in model[h]:
            p[c] += model[h][c]
            Z += model[h][c]
    for c in p:
        p[c] = p[c] / Z
    return p

def usage ():
    print ('usage: trigram-gen.py model N')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        file = sys.argv[1]
        N    = int (sys.argv[2]) 

    with open (file, 'rb') as f:
        model = pickle.load (f)
    model1 = unigram (model)
    for n in range(N):
        print (gen(model, model1))

if __name__ == "__main__":
    main ()
