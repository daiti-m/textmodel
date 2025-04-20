#!/usr/local/bin/python
#
#    bigram-gen.py
#    generation from bigram distributions.
#    $Id: bigram-gen.py,v 1.1 2020/11/11 00:26:17 daichi Exp $
#
import sys
import pickle
import numpy as np
from numpy.random import rand

BOS = '_BOS_'

def gen_char (dic, c):
    s = 0
    r = rand()
    for (d,p) in dic[c].items():
        s += p
        if (r < s):
            return d
    return d

def gen (model):
    s = ''
    c = BOS
    while True:
        c = gen_char (model, c)
        if (c == BOS):
            return s
        else:
            s += c

def usage ():
    print ('usage: bigram-gen.py model N')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        file = sys.argv[1]
        N    = int (sys.argv[2]) 

    with open (file, 'rb') as f:
        model = pickle.load (f)
    for n in range(N):
        print (gen(model))

if __name__ == "__main__":
    main ()
