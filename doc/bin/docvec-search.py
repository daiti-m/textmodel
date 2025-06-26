#!/usr/local/bin/python
#
#    docvec-search.py
#    $Id: docvec-search.py,v 1.1 2023/12/16 22:44:15 daichi Exp $
#
import sys
import docvec
import numpy as np
from pylab import *

def search (model, keywords):
    R = model['R']
    dic = model['dic']
    docvecs = normalize (model['docvec'])
    index = []
    # create virtual docvec
    print ('keyword:', end='')
    for word in keywords:
        if (word in dic):
            v = dic[word]
            index.append (v)
            print (' %s' % word, end='')
    print ('')
    if len(index) > 0:
        d = np.sum (R[:,index], axis=1)
    else:
        print ('no keyword in model!')
        sys.exit (0)
    # search
    N = docvecs.shape[0]
    cosines = np.dot (docvecs, d)
    return sorted (zip(range(N), cosines), key=lambda x: x[1], reverse=True)

def show (similars, text, M=15):
    N = len(similars)
    for i in range(M):
        n,score = similars[i]
        print ('% .4f\t%s' % (score, text[n][0:42]))
        if not (i < N):
            break

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
    print ('usage: % docvec-search.py model model.txt [keywords..]')
    print ('$Id: docvec-search.py,v 1.1 2023/12/16 22:44:15 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        model = docvec.load (sys.argv[1])
        text  = read (sys.argv[2])
        keywords = sys.argv[3:]

    # check
    if not (('dic' in model) and ('R' in model)):
        print ('both dictionary and regression matrix are required in the model.')
        sys.exit (1)

    # body
    similars = search (model, keywords)
    show (similars, text)


if __name__ == "__main__":
    main ()
