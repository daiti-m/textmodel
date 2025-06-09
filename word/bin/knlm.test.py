#!/usr/local/bin/python
#
#    knlm.test.py
#    prediction of Kneser-Ney n-gram language model. (given discount)
#    $Id: knlm.test.py,v 1.6 2021/05/20 12:43:02 daichi Exp $
#
import sys
import gzip
import pickle
import numpy as np
from pylab import *

def join (xx,rs):
    return rs.join (xx)

def predict (ngram, model):
    # prepare parameter
    nc = model['nc']
    nz = model['nz']
    nk = model['nk']
    rs = model['rs']
    V  = nk['']
    d  = 0.75
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

def parse (file, model):
    n = model['n']
    EOS = model['EOS']
    N   = 0
    lik = 0
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
                p = predict (ngram, model)
                lik += log (p)
                N   += 1
                print ('%s = %.6f' % (str(ngram), p))
    return exp (- lik / N)

def confirm (file, model):
    n = model['n']
    nc = model['nc']
    rs = model['rs']
    EOS = model['EOS']
    vocab = model['vocab']
    
    with open (file, 'r') as fh:
        for line in fh:
            # prepare words
            words = line.rstrip('\n').split()
            for t in range(n-1):
                words.insert (0, EOS)
            words.append (EOS)
            # parse
            T = len(words)
            for t in range(n-1, T):
                ngram = words[t-n+1:t+1]
                print ('ngram = %s' % str(ngram))
                print ('total = %f' % totalp(ngram,model,vocab))

def totalp (ngram, model, vocab):
    s = 0
    for word in vocab:
        ngram[-1] = word
        p = predict (ngram, model)
        s += p
    return s

def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model
                
def usage ():
    print ('knlm.test.py : prediction by Kneser-Ney n-gram language model.')
    print ('$Id: knlm.test.py,v 1.6 2021/05/20 12:43:02 daichi Exp $')
    print ('usage: % knlm-test.py test model')
    sys.exit (0)
    
def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        test = sys.argv[1]
        model = pload (sys.argv[2])

    print ('PPL = %.2f' % parse (test, model))
    # confirm (test, model)



if __name__ == "__main__":
    main ()
