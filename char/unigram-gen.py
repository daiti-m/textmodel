#!/usr/local/bin/python
#
#    unigram-gen.py
#    generation from a unigram distribution.
#    $Id: unigram-gen.py,v 1.1 2020/11/11 00:26:33 daichi Exp $
#
import sys
import pickle
import numpy as np
from numpy.random import rand

def gen_char (dic):
    s = 0
    r = rand()
    for (c,p) in dic.items():
        s += p
        if (r < s):
            return c
    return c

def gen (model, L):
    s = ''
    for i in range(L):
        s += gen_char (model)
    return s

def usage ():
    print ('usage: unigram-gen.py model N L')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        file = sys.argv[1]
        N    = int (sys.argv[2])
        L    = int (sys.argv[3])

    with open (file, 'rb') as f:
        model = pickle.load (f)
    for n in range(N):
        print (gen(model, L))

if __name__ == "__main__":
    main ()
