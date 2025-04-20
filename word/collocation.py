#!/usr/local/bin/python

import sys
import gzip
import pickle
import numpy as np
from eprint import eprint,eprintf

def info (counts, word):
    if not (word in counts):
        print ('%s does not exist.' % word)
    else:
        Z = sum (list(counts[word].values()))
        print ('%s:' % word)
        for cword,count in sorted (counts[word].items(),
                                   key=lambda x: x[1], reverse=True):
            print ('  %-8s -> %.4f  (%5d)' % (cword, count / Z, count))

def info2 (counts, word, target):
    if not (word in counts):
        print ('%s does not exist.' % word)
    else:
        p,c,Z = predict (counts, word, target)
        print ('p(%s|%s) = %.8f  (%d/%d)' % (target, word, p, c, Z))

def info3 (counts, word, word2, target):
    if not ((word in counts) and (word2 in counts)):
        print ('context does not exist.')
    else:
        p1,c1,Z1 = predict (counts, word, target)
        p2,c2,Z2 = predict (counts, word2, target)
        print ('p(%s|%s) = %.8f  (%d/%d)' % (target, word, p1, c1, Z1))
        print ('p(%s|%s) = %.8f  (%d/%d)' % (target, word2, p2, c2, Z2))
        print ('p(%s|%s)/p(%s|%s) = %.8f' % (target, word, target, word2, p1 / p2))
        

def predict (counts, word, target):
    if not (target in counts[word]):
        eprint ('count(%s|%s) does not exist.' % (target, word))
        sys.exit (0)
    c = counts[word][target]
    Z = sum (list(counts[word].values()))
    return c/Z, c, Z

def usage ():
    print ('usage: % collocation.py model word')
    print ('       % collocation.py model word target')
    print ('       % collocation.py model word word2 target')
    print ('$Id: collocation.py,v 1.2 2022/01/05 11:37:33 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        model = sys.argv[1]
        word  = sys.argv[2]
        word2 = sys.argv[3] if len(sys.argv) > 3 else None
        word3 = sys.argv[4] if len(sys.argv) > 4 else None
        
    with gzip.open (model, 'rb') as gf:
        eprint ('loading model from %s..' % model)
        counts = pickle.load (gf)

    if len(sys.argv) == 3:
        info (counts, word)
    elif len(sys.argv) == 4:
        info2 (counts, word, word2)
    elif len(sys.argv) == 5:
        info3 (counts, word, word2, word3)
    else:
        usage ()
    

if __name__ == "__main__":
    main ()
