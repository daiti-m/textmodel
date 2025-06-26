#!/usr/local/bin/python

import re
import os
import sys
import numpy as np
from os.path import join
from pylab import *

def save (corpus, file):
    print ('writing to %s.. ' % file)
    with open (file, 'w') as oh:
        for doc in corpus:
            oh.write (doc + '\n')
    print ('done.')

def read (dir):
    data = []
    for file in files (dir + '/pos'):
        data.append (parse (dir + '/pos/'+ file, 'positive'))
    for file in files (dir + '/neg'):
        data.append (parse (dir + '/neg/'+ file, 'negative'))
    return data

def parse (file, label):
    doc = ("%s\t" % label)
    with open (file, 'r') as fh:
        first = True
        for line in fh:
            tokens = line.rstrip('\n').split()
            words = list (filter (isvalid, tokens))
            if first:
                doc += ' '.join(words)
            else:
                doc += ' ' + ' '.join(words)
            first = False
    return doc

def files (dir):
    entries = sorted (os.listdir (dir))
    return filter (lambda x: os.path.isfile(join(dir, x)), entries)

def isvalid (word):
    return re.search (r"^[a-zA-Z][a-zA-Z']*$", word)

def usage ():
    print ('usage: % reviews.py txt_sentoken/ reviews.txt')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
        
    corpus = read (sys.argv[1])
    save (corpus, sys.argv[2])

if __name__ == "__main__":
    main ()
