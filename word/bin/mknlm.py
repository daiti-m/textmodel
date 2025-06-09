#!/usr/local/bin/python
#
#    mknlm.py
#    estimation of modified Kneser-Ney n-gram language model. (estimate discount)
#    $Id: mknlm.py,v 1.2 2021/05/20 12:45:42 daichi Exp $
#
import sys
import gzip
import pickle
import numpy as np
from collections import defaultdict

nc = defaultdict (int)
nz = defaultdict (int)
nk1 = defaultdict (int)
nk2 = defaultdict (int)
nk3 = defaultdict (int)
rs = '|' # "\034"
EOS = "_EOS_"

def count (ngram):
    global nc, nz, nk1, nk2, nk3
    hw = join (ngram)
    h  = join (ngram[0:-1])
    # add counts
    nz[h] += 1
    nc[hw] += 1
    if nc[hw] == 1:
        nk1[h] += 1
    elif nc[hw] == 2:
        nk2[h] += 1
        nk1[h] -= 1
    elif nc[hw] == 3:
        nk3[h] += 1
        nk2[h] -= 1
    # recurse if necessary
    if nc[hw] <= 3:
        if (len(ngram) > 1):
            count (ngram[1:])

def parse (file, n):
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
                count (ngram)

def mkn_discounts (file, n):
    D = []
    freq = []
    for i in range(n):
        freq.append (defaultdict(int))
    # count frequencies
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
                for i in range(n):
                    key = join (ngram[i:])
                    gram = n - i - 1
                    freq[gram][key] += 1
    # make discounts
    for i in range(n):
        D.append (mkn_discount (freq[i]))
    return D

def mkn_discount (freq):  # modified Kneser-Ney discounts
    n1 = 0; n2 = 0; n3 = 0; n4 = 0
    for s,c in freq.items():
        if c == 1:
            n1 += 1
        elif c == 2:
            n2 += 1
        elif c == 3:
            n3 += 1
        elif c == 4:
            n4 += 1
    Y = n1 / (n1 + 2 * n2)
    D1 = 1 - 2 * Y * n2 / n1
    D2 = 2 - 3 * Y * n3 / n2
    D3 = 3 - 4 * Y * n4 / n3
    return [D1, D2, D3]

def vocabulary (nc, rs):
    vocab = []
    for s,c in nc.items():
        n = s.count (rs)
        if (n == 0):
            vocab.append (s)
    return vocab
                
def join (xx):
    return rs.join (xx)

def save (file, train, n):
    global nc, nz, nk1, nk2, nk3
    model = { 'n' : n, 'rs' : rs, 'EOS' : EOS,
              'nc' : nc, 'nz' : nz, 'nk1' : nk1, 'nk2' : nk2, 'nk3' : nk3,
              'vocab' : vocabulary (nc, rs),
              'discounts' : mkn_discounts (train, n) }
    with gzip.open (file, 'wb') as gf:
        pickle.dump (model, gf)

def usage ():
    print ('mknlm.py : estimating modified Kneser-Ney n-gram language model.')
    print ('$Id: mknlm.py,v 1.2 2021/05/20 12:45:42 daichi Exp $')
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
    save  (model, train, n)

if __name__ == "__main__":
    main ()
