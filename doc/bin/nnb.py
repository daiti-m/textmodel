#!/usr/local/bin/python
#
#    nnb.py
#    Negation Naive Bayes (Komiya+ 2011) implementation.
#    $Id: nnb.py,v 1.2 2023/02/02 10:26:35 daichi Exp $
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

def nnb (texts, labels, alpha=0.01, threshold=10):
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
    qkv = np.zeros ((K,V), dtype=float)
    for n in range(N):
        text = texts[n]
        k    = labels[n]
        pk[k] += 1
        for word in text.split():
            if (word in vocab):
                v = vocab[word]
                for j in range(K):
                    if j != k:
                        qkv[j][v] += 1
    # smooth and normalize
    pk /= np.sum (pk)  # assume pk[k] != 0
    for k in range(K):
        qkv[k] += alpha
        qkv[k] /= np.sum (qkv[k])
    dic = {}
    for cat,label in cat2label.items():
        dic[cat] = label
    
    return { 'cat2label' : dic, 'K' : K, 'vocab' : vocab, 'pk' : pk, 'qkv' : qkv }

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
    print ('nnb.py : negation naive Bayes.')
    print ('usage: % nnb.py train model [alpha] [threshold]')
    print ('$Id: nnb.py,v 1.2 2023/02/02 10:26:35 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        alpha = float (sys.argv[3]) if len(sys.argv) > 3 else 0.01
        threshold = int (sys.argv[4]) if len(sys.argv) > 4 else 10
        
    texts,labels = load (sys.argv[1])
    model = nnb (texts, labels, alpha, threshold)
    save (model, sys.argv[2])


if __name__ == "__main__":
    main ()
