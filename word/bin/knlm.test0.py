#!/usr/local/bin/python

import sys
import gzip
import pickle
import numpy as np
from pylab import *

def join (xx,rs):
    return rs.join (xx)

def predict (ngram, model):
    # prepare parameter
    V = 1000
    d = 0.75
    nc = model['nc']
    nz = model['nz']
    nk = model['nk']
    rs = model['rs']
    # body
    if len(ngram) == 0:
        return 1 / V
    h = join (ngram[0:-1], rs)
    if (h in nz):
        hw = join (ngram, rs)
        if (hw in nc):
            p = (nc[hw] - d) / nz[h]
        else:
            p = 0
        return p + nk[h] * d / nz[h] * predict (ngram[1:], model)
    else:
        return predict (ngram[1:], model)

def predict0 (ngram, model):
    d = 0.75
    # prepare parameter
    nc = model['nc']
    nz = model['nz']
    nk = model['nk']
    rs = model['rs']
    # unigram
    w = ngram[-1]
    h = ''
    uni = nc[w] / nz[h]
    
    # bigram
    h = ngram[-2]
    if (h in nz):
        hw = join (ngram[-2:], rs)
        if (hw in nc):
            bi = (nc[hw] - d) / nz[h]
        else:
            bi = 0
        bi += nk[h] * d / nz[h] * uni
        
        # trigram
        h = join (ngram[-3:-1], rs)
        if (h in nz):
            hw = join (ngram, rs)
            if (hw in nc):
                tri = (nc[hw] - d) / nz[h]
            else:
                tri = 0
            tri += nk[h] * d / nz[h] * bi
            p = tri
        else:
            p = bi
    else:
        p = uni

    return p
    

def parse (file, model):
    n = model['n']
    EOS = model['EOS']
    with open (file, 'r') as fh:
        for line in fh:
            # prepare words
            words = line.rstrip('\n').split()
            for t in range(n-1):
                words.insert (0, EOS)
            words.append (EOS)
            print ("* sentence =", '|'.join(words))
            # parse
            T = len(words)
            for t in range(n-1, T):
                ngram = words[t-n+1:t+1]
                print ('%s = %.6f' % (str (ngram), predict (ngram, model)))

def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model
                
def usage ():
    print ('knlm.test.py : prediction by Kneser-Ney n-gram language model.')
    print ('$Id: knlm.test.py,v 1.2 2021/05/19 11:18:47 daichi Exp $')
    print ('usage: % knlm-test.py test model')
    sys.exit (0)
    
def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        test = sys.argv[1]
        model = pload (sys.argv[2])

    parse (test, model)



if __name__ == "__main__":
    main ()
