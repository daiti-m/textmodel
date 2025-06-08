#!/usr/local/bin/python
#
#    kfold-alpha.py
#    K-fold cross validation to select alpha from candidates.
#    $Id: kfold-alpha.py,v 1.4 2022/07/18 04:15:02 daichi Exp $
#

import sys
import bigram
import itertools
import numpy as np
from numpy import log,exp

def validate (text, K, alphas):
    data = load (text)
    for alpha in alphas:
        lik = 0
        N = 0        
        for train,test in kfold (data, K):
            model = bigram.parse_data (train, alpha)
            l,n = bigram.predict_data (model, test)
            lik += l
            N += n
        print ("alpha = %.4f : likelihood = %.2f (PPL = %.3f)" \
               % (alpha, lik, exp(-lik/N)))

def kfold (data, K):
    index = split (data, K)
    for k in range(K):
        test = index[k]
        train = flatten ([x for i,x in enumerate(index) if i != k])
        yield ([data[i] for i in train], [data[i] for i in test])

def split (data, K):
    N = len(data)
    size = int (N / K)
    index = []
    for k in range(K):
        if (k < K-1):
            index.append (list(range(k*size,(k+1)*size)))
        else:
            if (size * K == N):
                index.append (list(range(k*size,(k+1)*size)))
            else:
                index.append (list(range(k*size,N)))
    return index

#
# utility functions.
#

def flatten (xx):
    return list (itertools.chain(*xx))

def load (file):
    data = []
    with open (file, 'r') as fh:
        for buf in fh:
            line = buf.rstrip('\n')
            if len(line) > 0:
                data.append (line)
    return data

def usage ():
    print ('usage: % kfold-alpha.py K text alpha1 alpha2..')
    print ('$Id: kfold-alpha.py,v 1.4 2022/07/18 04:15:02 daichi Exp $')
    sys.exit(0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        K = int(sys.argv[1])
        text = sys.argv[2]
        alphas = list (map (float, sys.argv[3:]))

    validate (text, K, alphas)
    

if __name__ == "__main__":
    main ()
