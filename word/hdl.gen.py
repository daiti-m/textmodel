#!/usr/local/bin/python

import sys
import fmatrix
import numpy as np
from rutil import pmultinom
from numpy.random import rand
from pylab import *

def runif (alphas, dic):
    v = pmultinom (alphas)
    if (v in dic):
        return runif (alphas, dic)
    else:
        return v

def choose (dic):
    z = sum (list(dic.values()))
    r = rand()
    s = 0
    for v,c in dic.items():
        s += c
        if r <= (s / z):
            return v
    error ("choose: iteration exceeded")
    return list(dic.values())[0]

def gen_word (dic, alphas):
    nw = sum (list(dic.values()))
    alpha = sum (alphas)
    r = rand()
    if (r < nw / (nw + alpha)):
        return choose (dic)
    else:
        return runif (alphas, dic)

def gen_sentence (data, dic, alphas):
    EOS = '_EOS_'
    words = []
    p = 0
    while True:
        v = gen_word (data[p], alphas)
        # print ("v =", v)
        word = dic[v]
        if (word == EOS):
            break
        else:
            words.append (word)
            p = v
    print (''.join(words))

def gen (data, dic, alphas, N):
    V = len(dic)
    for n in range(N):
        gen_sentence (data, dic, alphas)

def dload (file):
    data = {}
    with open (file, 'r') as fh:
        for line in fh:
            label,content = line.split ('\t')
            w = int(label) - 1
            data[w] = {}
            tokens = content.split()
            for token in tokens:
                id,cnt = token.split(':')
                v = int(id) - 1
                c = int(cnt)
                data[w][v] = c
    return data

def dicload (file):
    dic = {}
    with open (file, 'r') as fh:
        for line in fh:
            id,word = line.rstrip('\n').split('\t')
            dic[int(id)-1] = word
    return dic

def vload (file):
    return np.loadtxt (file, dtype=float)

def usage ():
    print ('usage: % hdl.gen.py model{.dat,.dic,.alphas} N')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        data = dload (sys.argv[1] + '.dat')
        dic  = dicload (sys.argv[1] + '.dic')
        alphas = vload (sys.argv[1] + '.alphas')
        N      = int (sys.argv[2])

    gen (data, dic, alphas, N)


if __name__ == "__main__":
    main ()
