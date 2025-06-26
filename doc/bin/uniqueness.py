#!/usr/local/bin/python

import sys
import gzip
import pickle
import numpy as np
from collections import defaultdict

def uniqueness (topicwords):
    K = len(topicwords)
    tf = topicfreq (topicwords)
    tu = np.zeros (K, dtype=float)
    for k in range(K):
        tu[k] = unique (topicwords[k], tf)
    return np.mean (tu)

def topicfreq (topicwords):
    tf = defaultdict (int)
    for words in topicwords:
        for word in words:
            tf[word] += 1
    return tf

def unique (words, tf):
    s = 0
    for word in words:
        s += 1 / tf[word]
    return s / len(words)
    
def topwords (model, top=10):
    K,V = model['beta'].T.shape
    beta = model['beta'].T
    lexicon = tolexicon (model)
    topicwords = [set() for k in range(K)]
    for k in range(K):
        seen = 0
        for p,word in sorted (zip(beta[k], lexicon), key=lambda x: x[0], reverse=True):
            topicwords[k].add (word)
            seen += 1
            if (seen >= top):
                break
    return topicwords

def tolexicon (model):
    dic = {}
    lexicon = model['lexicon']
    for word,id in lexicon.items():
        dic[id] = word
    V = model['beta'].shape[0]
    return [(dic[v] if v in dic else "") for v in range(V)]

def load (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % uniqueness.py model [top]')
    print ('$Id: uniqueness.py,v 1.1 2023/06/13 10:33:55 daichi Exp $')
    sys.exit (0)


def main ():
    if len(sys.argv) < 2:
        usage ()
    else:
        model = load (sys.argv[1])
        top   = int (sys.argv[2]) if len(sys.argv) > 2 else 10
        
    topicwords = topwords (model, top)
    print ('TU = %.4f' % uniqueness (topicwords))


if __name__ == "__main__":
    main ()
