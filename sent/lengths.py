#!/usr/local/bin/python

import sys
import putil
import numpy as np
from opts import getopts
from ustring import ulength
from pylab import *

def plot_lengths (lengths, bins=20):
    putil.figsize ((6,3.5))
    putil.fontsize (18)
    hist (lengths, bins=bins,  color='black')
    xlabel ('length', fontsize=24, labelpad=8)
    ylabel ('frequency', fontsize=24, labelpad=11)
    
def parse (file, word=False, loglen=False):
    lengths = []
    with open (file, 'r') as fh:
        for line in fh:
            if word:
                n = len (line.rstrip('\n').split())
            else:
                sent = line.rstrip('\n').replace(' ', '')
                n = ulength(sent)
            if loglen:
                lengths.append (log(n))
            else:
                lengths.append (n)
    return lengths

def usage ():
    print ('usage: % length.py OPTIONS train.txt [output]')
    print ('OPTIONS')
    print ('-w   word-based counting (default chars, eliminating space)')
    print ('-l   logarithmic-scale density')
    print ('-L   logarithmic-scale sentence length')
    print ('$Id: length.py,v 1.4 2024/07/22 07:38:42 daichi Exp $')
    sys.exit (0)

def main ():
    opts,args = getopts (["l|log", "L|loglen", "w|word", "h|help"])
    if (len(args) < 1) or ('h' in opts):
        usage ()
    else:
        wordp = ('w' in opts)
        loglen = ('L' in opts)
        logscale = ('l' in opts)
        output = args[1] if len(args) > 1 else None
        
    lengths = parse (args[0], word=wordp, loglen=loglen)
    if output:
        with open (output, 'w') as oh:
            for length in lengths:
                oh.write ('%d\n' % length)
    else:
        print (lengths)


if __name__ == "__main__":
    main ()
