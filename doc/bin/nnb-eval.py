#!/usr/local/bin/python
#
#    nb-eval.py
#    $Id: nnb-eval.py,v 1.1 2023/02/02 10:26:44 daichi Exp $
#
import sys
import gzip
import pickle
import numpy as np
from pylab import *

def doclik (text, model, q):
    vocab = model['vocab']
    lik = 0
    for word in text.split():
        if (word in vocab):
            v = vocab[word]
            lik += log (q[v])
    return lik

def predict (text, model):
    K = model['K']
    pk = model['pk']
    qkv = model['qkv']
    liks = np.zeros (K, dtype=float)
    for k in range(K):
        liks[k] = log (1 - pk[k]) + doclik (text, model, qkv[k])
    return np.argmin (liks)

def evaluate (texts, labels, model):
    N = len(texts)
    correct = 0
    for n in range(N):
        text = texts[n]
        label = labels[n]
        k = predict (text, model)
        if (k == label):
            correct += 1
        # print ('predict = %d, true = %d' % (k, label))
    print ('accuracy = %.2f%%' % (correct / N * 100))

def load (file, model):
    texts = []
    labels = []
    cat2label = model['cat2label']
    with open (file, 'r') as fh:
        for line in fh:
            category,text = line.rstrip('\n').split('\t')
            label = cat2label[category]
            texts.append (text)
            labels.append (label)
    return texts, labels

def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % nb-eval.py test model')
    print ('$Id: nnb-eval.py,v 1.1 2023/02/02 10:26:44 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    model = pload (sys.argv[2])
    texts,labels = load (sys.argv[1], model)
    evaluate (texts, labels, model)


if __name__ == "__main__":
    main ()
