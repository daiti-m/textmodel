#!/usr/local/bin/python
# 
#    fmatrix.py : loading sparse feature matrix.
#    $Id: fmatrix.py,v 1.2 2023/03/13 00:01:24 daichi Exp $
# 
import sys
import numpy as np
from collections import defaultdict

class document:
    def __init__ (self):
        self.id  = []
        self.cnt = []
    def print (self):
        print ('doc:')
        print ('id  =', self.id)
        print ('cnt =', self.cnt)

def create (ids):
    doc = document ()
    freq = defaultdict (int)
    for id in ids:
        freq[id] += 1
    for id,count in sorted (freq.items(), key=lambda x: x[0]):
        doc.id.append (id)
        doc.cnt.append (count)
    return doc

def parse (file, origin=0):
    data = []
    with open (file, 'r') as fh:
        for line in fh:
            tokens = line.split()
            if len(tokens) > 0:
                doc = document()
                for token in tokens:
                    id,cnt = token.split(':')
                    doc.id.append (int(id) - origin)
                    doc.cnt.append (int(cnt))
                data.append (doc)
    return data

def plain (file, origin=0):
    """
    build a plain word sequence for LDA.
    """
    data = []
    with open (file, 'r') as fh:
        for line in fh:
            words = expand (line, origin)
            if len(words) > 0:
                data.append (words)
    return data

def full (file, origin=0):
    data = parse (file, origin)
    N,V = size (data)
    X = np.zeros ((N,V), dtype=int)
    for n in range(N):
        doc = data[n]
        X[n,doc.id] = doc.cnt
    return X

def expand (line, origin=0):
    words = []
    tokens = line.split()
    if len(tokens) > 0:
        for token in tokens:
            [id,cnt] = token.split(':')
            w = int(id) - origin
            c = int(cnt)
            words.extend ([w for x in range(c)])
        return words
    else:
        return []

def nnz (docs):
    n = 0
    for doc in docs:
        n += len (doc.cnt)
    return n

def size (docs):
    V = 0
    for doc in docs:
        if (max(doc.id) > V):
            V = max(doc.id)
    return len(docs), (V+1)

def main ():
    matrix = full (sys.argv[1], origin=1)
    data = parse (sys.argv[1], origin=1)
    elems = nnz (data)
    N,V = matrix.shape
    print (matrix[0:10,0:10])
    sys.stderr.write ('sparsity = %.2f %% (%d/%d)\n' %
                      ((1-elems/(N*V)) * 100, N*V-elems, N*V))
    
if __name__ == "__main__":
    main ()
    
