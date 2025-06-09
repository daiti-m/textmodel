#!/usr/local/bin/python
#
#    wordvector.py
#    $Id: wordvector.py,v 1.1 2020/09/15 12:16:07 daichi Exp $
#    computing word vector through a simple sparse SVD.
#

import re
import sys
import numpy as np
from opts import getopts
from eprint import eprint,eprintf
from collections import defaultdict
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import svds
from pylab import *

def parse (file, dic, width, k=1, alpha=0.75):
    data = []
    row  = []
    col  = []
    lines = 0
    datalen = 0
    V     = len (dic)
    p     = np.zeros (V, dtype=float)
    freq  = defaultdict (int)
    count = [defaultdict(int) for v in range(V)]
    eprint ('counting cooccurrences..')

    # read word frequency
    with open (file, 'r') as fh:
        for line in fh.readlines():
            if re.match(r'^[ \t\n]*$', line):
                continue
            words = line.rstrip('\n').split()
            # count frequency
            for word in words:
                if word in dic: # only frequency >= threshold
                    w = dic[word]
                    freq[w] += 1
                    datalen += 1
                    
    for w,c in freq.items():
        p[w] = c ** alpha
    p /= np.sum (p)

    # body
    with open (file, 'r') as fh:
        lines = 0
        for line in fh.readlines():
            if re.match(r'^[ \t\n]*$', line):
                continue
            lines += 1
            if (lines % 100) == 0:
                eprintf ('processing lines %3d..\r' % lines)
            # count
            words = line.rstrip('\n').split()
            T = len (words)
            for t in range(T):
                word = words[t]
                if word in dic:
                    v = dic[word]
                    for cword in window (words, t, width):
                        if cword in dic:
                            w = dic[cword]
                            count[v][w] += 1
    eprintf ('\n',clear=False)
                            
    print ('datalen = %d, lexicon = %d, k = %d' % (datalen, len(dic), k))
                            
    # summarize cooccurrences
    for v in range(V):
        if ((v+1) % 100 == 0):
            eprintf ('creating sparse matrix %4d/%d..\r' % (v+1,V))
        nwords = sum (list (count[v].values()))
        for w,c in count[v].items():
            pmi = log (c / (nwords * p[w]))
            val = pmi - log (k)
            if val > 0:
                data.append (val)
                row.append (v)
                col.append (w)
    eprintf ('creating sparse matrix %4d/%d..\n' % (V,V))
    # create sparse matrix
    X = coo_matrix ((data, (row, col)))
    return X

def window (words, t, width):
    st = t - width
    ed = t + width
    if (st < 0):
        st = 0
    if (ed > len(words) - 1):
        ed = len(words) - 1
    return words[st:t] + words[t+1:ed+1]

def compress (matrix, K):
    eprint ('computing SVD..')
    U,S,V = svds (matrix, k=K)
    return np.dot (U, diag(sqrt(S)))

def lexicon (file, threshold):
    eprint ('counting lexicon..')
    freq = defaultdict (int)
    lexicon = {}
    seed = 0
    with open (file, 'r') as fh:
        for line in fh.readlines():
            if re.match(r'^[ \t\n]*$', line):
                continue
            words = line.rstrip('\n').split()
            for word in words:
                freq[word] += 1

    for word,count in sorted (freq.items(), key=lambda x: x[1], reverse=True):
        if count >= threshold:
            lexicon[word] = seed
            seed += 1
    return lexicon

def analyze (file, K, window, k, threshold):
    dic = lexicon (file, threshold)
    matrix = parse (file, dic, window, k)
    vectors = compress (matrix, K)
    return vectors,dic

def save (vectors, file, dic):
    V,K = vectors.shape
    # create id -> word
    idword = {}
    for word,id in dic.items():
        idword[id] = word
    with open (file, 'w') as fh:
        for v in range(V):
            vec = vectors[v]
            fh.write ('%s\t' % idword[v])
            for k in range(K):
                fh.write ('%.5g%s' % (vec[k], ' ' if k < K-1 else '\n'))

def norm (x):
    return sqrt (np.dot(x,x))
    
def usage ():
    print ('usage: wordvector.py OPTIONS train model')
    print ('$Id: wordvector.py,v 1.1 2020/09/15 12:16:07 daichi Exp $')
    print ('OPTIONS')
    print ('-K dimensions number of word vector dimensions')
    print ('-w width      width of coocurrence window (before and after)')
    print ('-k k          number of pseudo negative samples (default 1)')
    print ('-t threshold  word frequency threshold to analyze (default 10)')
    print ('-h            displays this help')
    sys.exit (0)

def main ():
    opts,args = getopts (["K|latents=", "w|window=", "t|threshold=", "k|negatives=",
                          "h|help"])
    if len(args) < 2:
        usage ()
    else:
        text = args[0]
        model = args[1]
        K = int (opts['K']) if 'K' in opts else 10
        window = int (opts['w']) if 'w' in opts else 10
        negatives = int (opts['k']) if 'k' in opts else 1
        threshold = int (opts['t']) if 't' in opts else 10

    vectors,dic = analyze (text, K, window, negatives, threshold)
    save (vectors, model, dic)
    eprint ('done.')


if __name__ == "__main__":
    main ()
