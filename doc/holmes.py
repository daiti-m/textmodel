#!/usr/local/bin/python
#
#    novel.py
#    $Id: holmes.py,v 1.4 2023/04/11 13:07:15 daichi Exp $
#
import sys
import putil
import codecs
import numpy as np
from pylab import *

def draw (data, word):
    N = len(data)
    fig = figure (figsize=(6,2))
    plot (range(N), data, 'k')
    yticks ([0,1])
    xlabel ('  Time', fontsize=20, labelpad=5)
    axis ([0,N,0,1])
    
def find (text, target):
    N = len(text)
    occur = np.zeros (N, dtype=int)
    for n in range(N):
        if text[n] == target:
            occur[n] = 1
    return occur

def read (file):
    text = []
    with codecs.open (file, 'r', 'utf-8', 'ignore') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            if len(words) > 0:
                text += words
    return text            

def usage ():
    print ('usage: % holmes.py input.txt word [output]')
    print ('$Id: holmes.py,v 1.4 2023/04/11 13:07:15 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        text = sys.argv[1]
        target = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else None

    data = read (text)
    where = find (data, target)
    draw (where, target)
    if output is not None:
        putil.savefig (output, dpi=300)
    show ()


if __name__ == "__main__":
    main ()
