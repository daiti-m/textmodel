#!/usr/local/bin/python
#
#    nb.py
#    $Id: nb.py,v 1.5 2023/02/01 04:06:46 daichi Exp $
#
import sys
import gzip
import pickle
import numpy as np
from eprint import eprintf
from collections import defaultdict
cat2label = defaultdict (lambda: len(cat2label))

def vocabulary (texts, threshold):
    freq = defaultdict (int)
    vocab = {}
    id = 0
    for text in texts:
        words = text.split()
        for word in words:
            freq[word] += 1
    for word,count in sorted (freq.items(), key=lambda x: x[1], reverse=True):
        if count >= threshold:
            vocab[word] = id
            id += 1
    return vocab

def nb (texts, labels, alpha=0.01, threshold=10):
    vocab = vocabulary (texts, threshold)
    K = max (labels) + 1
    N = len (texts)
    V = len (vocab)
    eprintf ('N = %d docs, V = %d vocabs, K = %d classes.\n' % (N, V, K))
    eprintf ('alpha = %g, threshold = %d.\n' % (alpha, threshold))
    #
    #  body
    #
    pk = np.zeros (K, dtype=float)
    pkv = np.zeros ((K,V), dtype=float)
    for n in range(N):
        text = texts[n]
        k    = labels[n]
        pk[k] += 1
        for word in text.split():
            if (word in vocab):
                v = vocab[word]
                pkv[k][v] += 1
    # smooth and normalize
    pk /= np.sum (pk)  # assume pk[k] != 0
    for k in range(K):
        pkv[k] += alpha
        pkv[k] /= np.sum (pkv[k])
    dic = {}
    for cat,label in cat2label.items():
        dic[cat] = label
    
    return { 'cat2label' : dic, 'K' : K, 'vocab' : vocab, 'pk' : pk, 'pkv' : pkv }

def load (file):
    texts = []
    labels = []
    with open (file, 'r') as fh:
        for line in fh:
            category,text = line.rstrip('\n').split('\t')
            label = cat2label[category]
            texts.append (text)
            labels.append (label)
    return texts, labels

def save (model, file):
    eprintf ('saving model to %s.. ' % file)
    with gzip.open (file, 'wb') as gf:
        pickle.dump (model, gf)
    eprintf ('done.\n', clear=False)

def usage ():
    print ('usage: % nb.py train model [alpha] [threshold]')
    print ('$Id: nb.py,v 1.5 2023/02/01 04:06:46 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        alpha = float (sys.argv[3]) if len(sys.argv) > 3 else 0.01
        threshold = int (sys.argv[4]) if len(sys.argv) > 4 else 10
        
    texts,labels = load (sys.argv[1])
    model = nb (texts, labels, alpha, threshold)
    save (model, sys.argv[2])


if __name__ == "__main__":
    main ()
