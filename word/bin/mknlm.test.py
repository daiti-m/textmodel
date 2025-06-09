#!/usr/local/bin/python
#
#    mknlm.test.py
#    prediction of modified Kneser-Ney n-gram language model. (estimate discount)
#    $Id: mknlm.test.py,v 1.3 2021/05/20 13:51:42 daichi Exp $
#
import sys
import gzip
import pickle
import numpy as np
from pylab import *

def discount (c, n, D):
    if c == 0:
        return 0
    elif c == 1:
        return D[n-1][0]
    elif c == 2:
        return D[n-1][1]
    else:
        return D[n-1][2]

def predict (ngram, model):
    # prepare parameter
    nc  = model['nc']
    nz  = model['nz']
    nk1 = model['nk1']
    nk2 = model['nk2']
    nk3 = model['nk3']        
    rs  = model['rs']
    V   = len (model['vocab'])
    D   = model['discounts']
    n   = len(ngram)
    # body
    if n == 0:
        return 1 / V
    h = join (ngram[0:-1], rs)
    if (h in nz):
        hw = join (ngram, rs)
        if (hw in nc):
            d = discount (nc[hw], n, D)
            p = (nc[hw] - d) / nz[h]
        else:
            p = 0
        ds = nk1[h] * D[n-1][0] + nk2[h] * D[n-1][1] + nk3[h] * D[n-2][2]
        return p + ds / nz[h] * predict (ngram[1:], model)
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
                print ('total = %f' % totalp (ngram,model,vocab))

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
                
def join (xx,rs):
    return rs.join (xx)

def usage ():
    print ('mknlm.test.py : prediction by modified Kneser-Ney n-gram language model.')
    print ('$Id: mknlm.test.py,v 1.3 2021/05/20 13:51:42 daichi Exp $')
    print ('usage: % mknlm.test.py test model')
    sys.exit (0)
    
def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        test = sys.argv[1]
        model = pload (sys.argv[2])

    # print ('PPL = %.2f' % parse (test, model))
    confirm (test, model)



if __name__ == "__main__":
    main ()
