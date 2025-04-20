#!/usr/local/bin/python
#
#    bhmm - Bayesian HMM in Python.
#    $Id: bhmm.py,v 1.2 2023/05/13 23:55:29 daichi Exp $
#
import hmm
import sys
import gzip
import pickle
import numpy as np
from opts import getopts
from collections import defaultdict

def read (file, threshold):
    sys.stderr.write ('reading data from %s.. ' % file),
    sys.stderr.flush ()
    dic = lexicon (file, threshold)
    data = []
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            if len(words) > 0:
                data.append (list (map (lambda word: wordid(word, dic), words)))
    sys.stderr.write ('done.\n')
    return data, rdic(dic)

def lexicon (file, threshold):
    dic = {}
    seed = 0
    dic['_OOV_'] = seed
    freq = defaultdict (int)
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            for word in words:
                freq[word] += 1
    # build lexicon
    for word,count in sorted (freq.items(), key=lambda x: x[1], reverse=True):
        if (count >= threshold):
            seed += 1
            dic[word] = seed
    return dic

def wordid (word, dic):
    if (word in dic):
        return dic[word]
    else:
        return 0

def rdic (dic):
    rdic = {}
    for word,id in dic.items():
        rdic[id] = word
    return rdic

def save (model, dic, output):
    eprintf ('saving model to %s.. ' % output)
    model['dic'] = dic
    with gzip.open (output, 'wb') as gf:
        pickle.dump (model, gf, 2)
    eprintf ('done.\n')
    
def rnormalize (M): # row-wise normalize matrix
    return np.array ([m / np.sum(m) for m in M])

def eprint (s):
    sys.stderr.write (s + '\n')
    sys.stderr.flush ()

def eprintf (s):
    sys.stderr.write (s)
    sys.stderr.flush ()

def usage ():
    print ('bhmm.py: Bayesian HMM in Python.')
    print ('usage: % bhmm.py OPTIONS train model')
    print ('OPTIONS')
    print (' -G         use Gibbs sampling instead of dynamic programming')
    print (' -K states  number of states in HMM')
    print (' -N iters   number of MCMC iterations')
    print (' -a alpha   Dirichlet hyperparameter on transitions (default 0.1)')
    print (' -b beta    Dirichlet hyperparameter on emissions (default 0.01)')
    print (' -t thresh  Frequency threshold for lexicon (default 1)')    
    print (' -h         displays this help')
    print ('$Id: bhmm.py,v 1.2 2023/05/13 23:55:29 daichi Exp $')
    sys.exit (0)

def main ():
    opts,args = getopts (["K|states=", "N|iters=", "a|alpha=", "b|beta=",
                          "t|threshold=", "G|gibbs", "h|help"])
    if (len(args) != 2) or ('h' in opts):
        usage ()
    else:
        train = args[0]
        output = args[1]
        K = int (opts['K']) if 'K' in opts else 10
        iters = int (opts['N']) if 'N' in opts else 1
        alpha = float (opts['a']) if 'a' in opts else 0.1
        beta  = float (opts['b']) if 'b' in opts else 0.01
        threshold = int (opts['t']) if 't' in opts else 1
        gibbs = True if 'G' in opts else False

    data,dic = read (train, threshold)

    print ('data: %d sequences, lexicon: %d words.' % (len(data), len(dic)))    
            
    if gibbs:
        model = hmm.gibbs (data, K, alpha, beta, iters, output)
    else:
        model = hmm.learn (data, K, alpha, beta, iters, output)
        
    save (model, dic, output)

if __name__ == "__main__":
    main ()
