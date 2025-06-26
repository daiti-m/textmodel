#!/usr/local/bin/python

import sys
from collections import defaultdict

def parse (file, category, nshow=None):
    freq = defaultdict (int)
    with open (file, 'r') as fh:
        for line in fh:
            label,words = line.rstrip('\n').split('\t')
            if (label == category):
                for word in words.split():
                    freq[word] += 1
    # words for the category
    N = sum (freq.values())
    shown = 0
    for word,count in sorted (freq.items(), key=lambda x: x[1],
                              reverse=True):
        p = count / N
        print ('%s\t-> %.6f' % (word, p))
        shown += 1
        if (nshow is not None) and (shown > nshow):
            break
    
def usage ():
    print ('usage: % nbprob.py text category [maxshow]')
    print ('$Id$')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    nshow = int (sys.argv[3]) if len(sys.argv) > 3 else None
    parse (sys.argv[1], sys.argv[2], nshow)

if __name__ == "__main__":
    main ()
