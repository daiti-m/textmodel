#!/usr/local/bin/python

import sys
import docvec
import numpy as np
from pylab import *

def save_w2v (model, file):
    wordvec = model['featvec']
    dic = rdict (model['dic'])
    V,K = wordvec.shape
    # save
    print ('saving to %s..' % file)
    with open (file, 'w') as oh:
        for v in reversed(range(1,V)):
            oh.write ('%s\t' % dic[v])
            for k in range(K):
                oh.write ('% .7f%s' % (wordvec[v][k], '\n' if k==K-1 else ' '))
    print ('done.')
            

def rdict (dic):
    rdic = {}
    for key,val in dic.items():
        rdic[val] = key
    return rdic


def usage ():
    print ('usage: % docvec-word2vec.py model output')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
        
    model = docvec.load (sys.argv[1])
    save_w2v (model, sys.argv[2])



if __name__ == "__main__":
    main ()
