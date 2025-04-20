#!/usr/local/bin/python

import sys
import gzip
import pickle
import numpy as np
from pylab import *

def show_emission (model, k):
    betas = model['emit']
    dic = model['dic']
    words = [dic[v] for v in range(len(dic))]
    K = betas.shape[0]
    if k is not None:
        show_beta (betas, words, k)
    else:
        for k in range(K):
            show_beta (betas, words, k)
            print ('')
            
def show_beta (betas, words, k, nshow=10):
    beta = betas[k]
    shown = 0
    print ('[state %d]' % (k+1))
    for word,p in sorted (zip (words, beta), key=lambda x: x[1], reverse=True):
        print ('%-10s %.4f' % (word, p))
        shown += 1
        if shown > nshow:
            break

def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % emission.py model [k]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    model = pload (sys.argv[1])
    k = int (sys.argv[2]) - 1 if len(sys.argv) > 2 else None

    show_emission (model, k)


if __name__ == "__main__":
    main ()
