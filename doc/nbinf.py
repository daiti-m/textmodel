#!/usr/local/bin/python
#
#    nb-inf.py
#    $Id: nbinf.py,v 1.2 2024/04/06 01:47:37 daichi Exp $
#
import sys
import gzip
import pickle
import numpy as np
from pylab import *
from rutil import lnormalize

def doclik (text, model, p):
    vocab = model['vocab']
    lik = 0
    for word in text:
        if (word in vocab):
            v = vocab[word]
            lik += log (p[v])
    return lik

def infer (texts, labels, model):
    K = model['K']
    pk = model['pk']
    pkv = model['pkv']
    liks = np.zeros (K, dtype=float)
    N = len(texts)
    for n in range(N):
        text = texts[n]
        label = labels[n]
        for k in range(K):
            liks[k] = log (pk[k]) + doclik (text, model, pkv[k])
        print (label, lnormalize(liks), ''.join(text[0:15]))

def load (file):
    texts = []
    labels = []
    with open (file, 'r') as fh:
        for line in fh:
            label,text = line.rstrip('\n').split('\t')
            words = text.split()
            labels.append (label)
            texts.append (words)
    return labels, texts

def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % nbinf.py model text.txt')
    print ('$Id: nbinf.py,v 1.2 2024/04/06 01:47:37 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    model = pload (sys.argv[1])
    print (model['cat2label'])
    labels,texts = load (sys.argv[2])
    infer (texts, labels, model)

if __name__ == "__main__":
    main ()
