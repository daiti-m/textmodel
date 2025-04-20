#!/usr/local/bin/python
#
#    absolute.py: empirical validation of absolute discounting.
#    $Id: absolute.py,v 1.1 2022/01/21 00:37:19 daichi Exp $
#
import sys
import putil
import numpy as np
from collections import defaultdict
from pylab import *

EOS = '_EOS_'

def plot_data (data):
    cmax = 10
    stat = np.zeros (cmax + 1, dtype=float)
    for c,e in data.items():
        if c <= cmax:
            stat[c] = e
    xx = list(range(1,cmax+1))
    # plot
    figure (figsize=(6,4))
    putil.fontsize (20)
    plot (xx, stat[1:cmax+1])
    plot (xx, xx, color='k')
    xlabel ('$c$', fontsize=28, labelpad=0)
    ylabel ('$E[c]$', fontsize=28, rotation=0, labelpad=29)

def stat (first, second):
    data = {}
    freq = defaultdict (int)
    items = defaultdict (int)
    for word,count in first.items():
        newcount = second[word]
        freq[count] += newcount
        items[count] += 1
    for count in sorted (freq.keys()):
        e = freq[count] / items[count]
        data[count] = e
        if count <= 20:
            print ('%4d %6.2f (%4d) diff = % .2f' % (count, e, freq[count], count - e))
    return data

def parse (file, n, half):
    nwords = 0
    first = defaultdict (int)
    second = defaultdict (int)
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            for gram in ngram (n, words):
                nwords += 1
                word = join (gram)
                if nwords <= half:
                    first[word] += 1
                else:
                    second[word] += 1
    return first, second

def ngram (n, words):
    if n > 1: # >= bigram
        for i in range(n-1):
            words.insert (0, EOS)
        words.append (EOS)
        T = len(words)
        for t in range(T-1):
            yield words[t:t+n]
    else:	  # unigram
        for word in words:
            yield word

def nwords (file, n):
    N = 0
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            for gram in ngram (n, words):
                N += 1
    return N

def join (xx, sep='|'):
    if type(xx) is list:
        return sep.join (xx)
    else:
        return xx

def usage ():
    print ('usage: % absolute.py n text [output]')
    print ('$Id: absolute.py,v 1.1 2022/01/21 00:37:19 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        n = int (sys.argv[1])
        file = sys.argv[2]

    N = nwords (file, n)
    half = int (N / 2)
    print ('N = %d, half = %d' % (N, half))
    first,second = parse (file, n, half)
    data = stat (first, second)
    plot_data (data)
    
    if len(sys.argv) > 3:
        putil.savefig (sys.argv[3], dpi=300)
    show ()
    









if __name__ == "__main__":
    main ()
