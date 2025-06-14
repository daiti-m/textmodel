#!/usr/local/bin/python
#
#    knlm.gen.py
#    generation from Kneser-Ney n-gram language model. (given discount)
#    $Id: knlm.gen.py,v 1.3 2021/05/23 03:54:24 daichi Exp $
#
import sys
import gzip
import pickle
import numpy as np
from eprint import eprint, eprintf
from rutil import multinom
from pylab import *

def gen (model, N, sep=""):
    n = model['n']
    EOS = model['EOS']
    output = []
    # generate
    for i in range(N):
        word = ''
        words = []
        for t in range(n-1):
            words.append (EOS)
        while word != EOS:
            word = sample (words[-(n-1):], model)
            words.append (word)
            eprintf ('generating %d words..\r' % len(words))
            if len(words) > 100:
                eprint ('TOO LONG TO GENERATE!')
                break
        eprintf ('')
        sentence = sep.join (words[n-1:-1])
        print (sentence)
            
def sample (ngram, model):
    vocab = model['vocab']
    V = len(vocab)
    p = np.zeros (V, dtype=float)
    ngram.append ('')
    for v in range(V):
        ngram[-1] = vocab[v]
        p[v] = predict (ngram, model)
    return vocab [multinom(p)]
    # return vocab [nucleus(p, 0.95)]

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

def discount (c, n, D):
    if c == 0:
        return 0
    elif c == 1:
        return D[n-1][0]
    elif c == 2:
        return D[n-1][1]
    else:
        return D[n-1][2]

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

def nucleus (p, threshold=0.95):
    index = np.argsort (-p)
    N = len(p)
    K = 0
    s = 0
    for i in range(N):
        s += p[index[i]]
        if (s > threshold):
            K = i + 1
            break
    k = multinom (p[index[0:K]])
    return index[k]

def pload (file):
    eprintf ('loading model.. ')
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    eprintf ('done.\n', clear=False)
    return model
                
def join (xx,rs):
    return rs.join (xx)

def usage ():
    print ('mknlm.gen.py : generation from modified Kneser-Ney n-gram language model.')
    print ('$Id: knlm.gen.py,v 1.3 2021/05/23 03:54:24 daichi Exp $')
    print ('usage: % mknlm.gen.py model N [sep]')
    sys.exit (0)
    
def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        model = pload (sys.argv[1])
        N     = int (sys.argv[2])
        sep   = sys.argv[3] if len(sys.argv) > 3 else " "

    gen (model, N, sep)


if __name__ == "__main__":
    main ()
