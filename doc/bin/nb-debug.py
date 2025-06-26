#!/usr/local/bin/python
#
#    nb-eval.py
#    $Id: nb-eval.py,v 1.3 2023/02/01 02:33:19 daichi Exp $
#
import sys
import gzip
import pickle
import numpy as np
from pylab import *

def doclik (text, model, p):
    vocab = model['vocab']
    lik = 0
    for word in text.split():
        if (word in vocab):
            v = vocab[word]
            lik += log (p[v])
    return lik

def predict (text, model):
    K = model['K']
    pk = model['pk']
    pkv = model['pkv']
    liks = np.zeros (K, dtype=float)
    for k in range(K):
        liks[k] = log (pk[k]) + doclik (text, model, pkv[k])
    return np.argmax (liks)

def evaluate (texts, labels, model):
    # prepare
    cat2label = model['cat2label']
    label2cat = {}
    for cat,label in cat2label.items():
        label2cat[label] = cat
    # body
    N = len(texts)
    correct = 0
    for n in range(N):
        text = texts[n]
        label = labels[n]
        k = predict (text, model)
        if (k == label):
            correct += 1
        if (k != label):
            print ('%s\t%s\t%s' % (label2cat[label], label2cat[k], text.replace(' ', '')))
        # print ('predict = %d, true = %d' % (k, label))
    # print ('accuracy = %.2f%%' % (correct / N * 100))

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
    print ('$Id: nb-eval.py,v 1.3 2023/02/01 02:33:19 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    model = pload (sys.argv[2])
    texts,labels = load (sys.argv[1], model)
    evaluate (texts, labels, model)


if __name__ == "__main__":
    main ()
