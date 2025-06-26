#!/usr/local/bin/python
#
#    docvec.py
#    compute document vectors with simple SVD.
#    $Id: docvec.py,v 1.2 2023/12/16 14:51:51 daichi Exp $
#
import sys
import gzip
import pickle
import fmatrix
import numpy as np
from opts import getopts
from eprint import eprint,eprintf
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import svds
from collections import defaultdict
from pylab import *

def parse (docs):
    N    = len(docs)
    row  = []
    col  = []
    data = []
    freq = defaultdict (int)
    datalen = 0
    k = 1
    # prepare statistics
    for doc in docs:
        L = len (doc.id)
        for i in range(L):
            v = doc.id[i]
            c = doc.cnt[i]
            freq[v] += c
            datalen += c
    # parse
    for n in range(N):
        doc = docs[n]
        L   = len (doc.id)
        s   = sum (doc.cnt)
        for i in range(L):
            v = doc.id[i]
            c = doc.cnt[i]
            pmi = log (c * datalen / (float(s) * freq[v]))
            val = pmi - log (k)
            if val > 0:
                data.append (val)
                row.append (n)
                col.append (v)
    # create matrix
    X = coo_matrix ((data, (row, col)))
    return X

def compress (matrix, K):
    U,S,V = svds (matrix, k=K)
    return (np.dot (U, diag(sqrt(S))), np.dot(V.T, diag(sqrt(S))))

def parsedic (file):
    dic = {}
    with open (file, 'r') as fh:
        for line in fh:
            tokens = line.rstrip('\n').split('\t')
            id = int(tokens[0]); word = tokens[1]
            dic[word] = id
    return dic

def analyze (train, K, dic, reg):
    eprint ('parsing data..')
    data = fmatrix.parse (train)
    eprint ('creating sparse matrix..')
    matrix = parse (data)
    eprint ('computing data vectors..')
    docvec, featvec = compress (matrix, K)
    if dic:
        features = parsedic (dic)
    if reg:
        eprint ('computing regression matrix..')
        R = solve (np.dot (featvec.T, featvec), featvec.T)
    eprint ('done.')
    # create model
    model = { 'docvec': docvec, 'featvec': featvec }
    if dic:
        model['dic'] = features
    if reg:
        model['R'] = R
    return model

def save (model, file):
    with gzip.open (file, 'wb') as gf:
        eprint ('writing model to %s..' % file)
        pickle.dump (model, gf)
        eprint ('done.')

def load (file):
    with gzip.open (file, 'rb') as gf:
        eprintf ('loading model from %s.. ' % file)
        model = pickle.load (gf)
        eprintf ('done.\n')
    return model
        
def usage ():
    print ('usage: docvec.py OPTIONS train model')
    print ('$Id: docvec.py,v 1.2 2023/12/16 14:51:51 daichi Exp $')
    print ('OPTIONS')
    print ('-K dimenstions  number of document vector dimensions')
    print ('-R              also compute regression matrix')
    print ('-d dict         dictionary of id -> word mapping')
    print ('-h              displays this help')
    sys.exit (0)

def main ():
    opts,args = getopts (["K|latents=", "R|regression", "d|dict=", "h|help"])

    if len(args) < 2:
        usage ()
    else:
        train = args[0]
        file  = args[1]
        dic   = opts['d'] if 'd' in opts else None
        reg   = True if 'R' in opts else False
        K = int (opts['K']) if 'K' in opts else 10
        print ('using dictionary: %s' % dic) if dic is not None else {}
        print ('%s: K = %d, output = %s' % (train, K, file))

    model = analyze (train, K, dic, reg)
    save (model, file)
        
if __name__ == "__main__":
    main ()
