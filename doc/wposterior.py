#!/usr/local/bin/python

import sys
import numpy as np
from numpy import exp,log
from collections import defaultdict

def normalize (xx):
    return np.array (xx) / np.sum(xx)

def parse (file):
    pkv,pk = load (file)
    labels = ['positive', 'negative']
    words = set(pkv['positive'].keys()) | set(pkv['negative'].keys())
    unigram = compute_unigram (pkv, words)
    print ('%-13s %-8s %-8s |  %s' % ('word', 'positive', 'negative', 'r'))
    print ('-' * 41)
    for word in words:
    # for word in sorted(words):
    # for word in sorted (words, key=lambda x: unigram[x], reverse=True):
        p = [pk[label] * pkv[label][word] for label in labels]
        p = normalize (p)
        r = log (p[0]) - log (p[1])
        print ('%-13s %.4f   %.4f   | % .4f' % (word, p[0], p[1], r))
    
def compute_unigram (pkv, words):
    p = defaultdict (float)
    labels = pkv.keys()
    for word in words:
        p[word] = sum ([pkv[label][word] for label in labels])
    Z = sum (p.values())
    for word,val in p.items():
        p[word] = val / Z
    return p

def load (file):
    p = {}
    q = defaultdict (int)
    with open (file, 'r') as fh:
        for line in fh:
            label,words = line.rstrip('\n').split('\t')
            q[label] += 1
            if not (label in p):
                p[label] = defaultdict (int)
            for word in words.split():
                p[label][word] += 1
    # words for the category
    for label in p.keys():
        N = sum (p[label].values())
        for word,count in p[label].items():
            p[label][word] = count / N
    # category prior
    N = sum (q.values())
    for label,c in q.items():
        q[label] = c / N
    return p, q




def usage ():
    print ('usage: % wposterior.py input.txt')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    parse (sys.argv[1])



if __name__ == "__main__":
    main ()
