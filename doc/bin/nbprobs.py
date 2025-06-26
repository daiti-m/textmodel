#!/usr/local/bin/python

import sys
from collections import defaultdict

def parse (file):
    p = {}
    with open (file, 'r') as fh:
        for line in fh:
            label,words = line.rstrip('\n').split('\t')
            if not (label in p):
                p[label] = defaultdict (int)
            for word in words.split():
                p[label][word] += 1
    # words for the category
    for label in p.keys():
        N = sum (p[label].values())
        for word,count in p[label].items():
            p[label][word] = count / N
    return p
    
def usage ():
    print ('usage: % nbprobs text word')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    probs = parse (sys.argv[1])
    word = sys.argv[2]
    for label in probs.keys():
        print ('%-14s -> %.8f' % (label, probs[label][word]))
    

if __name__ == "__main__":
    main ()
