#!/usr/local/bin/python

import sys
from collections import defaultdict

def parse (file, interval):
    freq = defaultdict (int)
    nwords = 0
    
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            for word in words:
                freq[word] += 1
                nwords += 1
                if ((nwords < interval) and (nwords % 1000) == 0) or \
                   ((nwords % interval) == 0):
                    print ('%d\t%d' % (nwords, len(freq)))
    print ('%d\t%d' % (nwords, len(freq)))

def usage ():
    print ('usage: % progress-vocabulary.py text')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    else:
        file = sys.argv[1]
        interval = 1000 if len(sys.argv) < 3 else int(sys.argv[2])

    parse (file, interval)
                                                                          
if __name__ == "__main__":
    main ()
