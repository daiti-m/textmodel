#!/usr/local/bin/python

import sys
import fmatrix
import numpy as np
from collections import defaultdict
from pylab import *

def compute_idf (data):
    N = len(data)
    df = defaultdict (int)
    idf = {}
    # compute df
    for n in range(N):
        doc = data[n]
        for v in doc.id:
            df[v] += 1
    # compute idf
    for v,c in df.items():
        # idf[v] = log (N) - log (c)
        idf[v] = float(c) / N
    return idf

def tfidf (data, dic):
    N = len(data)
    idf = compute_idf (data)
    for v,val in sorted (idf.items(), key=lambda x: x[1], reverse=True):
        # print ('%s\t\t%.6f\t%.6f' % (dic[v], val, -log(val)))
        print ('%s\t& %.4f\t& %.4f \\\\' % (dic[v], val, -log(val)))


def loaddic (file):
    dic = {}
    with open (file, 'r') as fh:
        for line in fh:
            id,word = line.rstrip('\n').split('\t')
            dic[int(id)] = word
    return dic

def usage ():
    print ('usage: % tfidf.py livedoor{.dat,.lex} [output]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()

    data = fmatrix.parse (sys.argv[1] + '.dat')
    dic = loaddic (sys.argv[1] + '.lex')

    tfidf (data, dic)
    





if __name__ == "__main__":
    main ()
