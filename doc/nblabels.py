#!/usr/local/bin/python

import sys
from collections import defaultdict

def parse (file):
    docs = defaultdict (int)
    with open (file, 'r') as fh:
        for line in fh:
            label,words = line.rstrip('\n').split('\t')
            docs[label] += 1
    N = sum (docs.values())
    # labels
    for label,count in docs.items():
        print ('%-12s\t%.4f' % (label, count / N))
    
def usage ():
    print ('usage: % nbcount.py text')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    parse (sys.argv[1])

if __name__ == "__main__":
    main ()
