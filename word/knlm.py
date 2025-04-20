#!/usr/local/bin/python
#
#    knlm.py
#    estimation of Kneser-Ney n-gram language model. (given discount)
#    $Id: knlm.py,v 1.6 2021/05/23 02:50:59 daichi Exp $
#
import sys
import gzip
import pickle
import numpy as np
from eprint import eprintf
from collections import defaultdict

nc = defaultdict (int)
nz = defaultdict (int)
nk = defaultdict (int)
rs = '|' # "\034"
EOS = "_EOS_"

def count (ngram):
    global nc, nz, nk
    hw = join (ngram)
    h  = join (ngram[0:-1])
    nz[h] += 1
    nc[hw] += 1
    if nc[hw] == 1:
        nk[h] += 1
        if (len(ngram) > 1):
            count (ngram[1:])

def parse (file, n):
    lines = 0
    with open (file, 'r') as fh:
        for line in fh:
            lines += 1
            if (lines % 1000) == 0:
                eprintf ('reading %4d sentences..\r' % lines)
            # prepare words
            words = line.rstrip('\n').split()
            for t in range(n-1):
                words.insert (0, EOS)
            words.append (EOS)
            # print ("* sentence =", '|'.join(words))
            # parse
            T = len(words)
            for t in range(n-1, T):
                ngram = words[t-n+1:t+1]
                count (ngram)
    eprintf ('reading %4d sentences.. done.\n' % lines)

def vocabulary (nc, rs):
    vocab = []
    for s,c in nc.items():
        n = s.count (rs)
        if (n == 0):
            vocab.append (s)
    return vocab
                
def join (xx):
    return rs.join (xx)

def save (file, n, nc, nz, nk):
    eprintf ('writing model to %s.. ' % file)
    model = { 'n' : n, 'rs' : rs, 'EOS' : EOS,
              'nc' : nc, 'nz' : nz, 'nk' : nk,
              'vocab' : vocabulary (nc, rs) }
    with gzip.open (file, 'wb') as gf:
        pickle.dump (model, gf)
    eprintf ('done.\n', clear=False)

def usage ():
    print ('knlm.py : estimating Kneser-Ney n-gram language model.')
    print ('$Id: knlm.py,v 1.6 2021/05/23 02:50:59 daichi Exp $')
    print ('usage: % knlm.py n train model')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        n = int (sys.argv[1])
        train = sys.argv[2]
        model = sys.argv[3]

    parse (train, n)
    save  (model, n, nc, nz, nk)

if __name__ == "__main__":
    main ()
