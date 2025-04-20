#!/usr/local/bin/python

import sys
from collections import defaultdict

def parse (file, category):
    freq = defaultdict (int)
    with open (file, 'r') as fh:
        for line in fh:
            label,words = line.rstrip('\n').split('\t')
            if (label == category):
                for word in words.split():
                    freq[word] += 1
    # words for the category
    N = sum (freq.values())
    for word,count in sorted (freq.items(), key=lambda x: x[1],
                              reverse=True):
        p = count / N
        print ('%s\t-> %.6f' % (word, p))
    
def usage ():
    print ('usage: % nbcount.py text category')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    parse (sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main ()
