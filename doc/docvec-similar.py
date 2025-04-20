#!/usr/local/bin/python
#
#    docvec-similar.py
#    $Id: docvec-similar.py,v 1.4 2023/12/16 11:12:19 daichi Exp $
#
import sys
import docvec
import numpy as np
from pylab import *

def show (similars, text, M=15):
    N = len(similars)
    for i in range(M):
        n,score = similars[i]
        # print ('% .4f\t%s' % (score, text[n][0:42]))
        print ('% .4f\t%s' % (score, text[n][0:39]))
        if not (i < N):
            break

def search (docvecs, n): # n begins from 1
    N = docvecs.shape[0]
    n = n - 1
    cosines = np.dot (docvecs, docvecs[n])
    return sorted (zip(range(N), cosines), key=lambda x: x[1], reverse=True)

def normalize (X):
    s = sqrt (sum (X * X, axis=1))
    return dot (diag (1/s), X)

def read (file):
    text = []
    with open (file, 'r') as fh:
        for line in fh:
            label,body = line.rstrip('\n').split('\t')
            text.append ('%-14s %s' % (label, body.replace(' ', '')))
    return text

def usage ():
    print ('usage: % docvec-similar.py model model.txt n')
    print ('$Id: docvec-similar.py,v 1.4 2023/12/16 11:12:19 daichi Exp $')
    sys.exit (0)
    
def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        model = docvec.load (sys.argv[1])
        text  = read (sys.argv[2])
        n = int (sys.argv[3])

    docvecs = normalize (model['docvec'])
    similars = search (docvecs, n)
    show (similars, text)

if __name__ == "__main__":
    main ()
