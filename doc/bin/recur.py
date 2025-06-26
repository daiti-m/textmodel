#!/usr/local/bin/python

import sys
import numpy as np
from pylab import *

def find (words, keyword):
    N = len(words)
    half = int (N/2)
    train,test = words[0:half], words[half:]
    istrain = sum ([word == keyword for word in train])
    istest  = sum ([word == keyword for word in test])
    a = (istrain > 0) and (istest > 0)
    b = (istrain > 0) and (istest == 0)
    c = (istrain == 0) and (istest > 0)
    d = (istrain == 0) and (istest == 0)
    return list (map (int, [a,b,c,d]))

def parse (file, keyword):
    occurs = np.array ([0,0,0,0])
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            if len(words) > 0:
                occur = find (words, keyword)
                occurs += occur
    return occurs

def usage ():
    print ('usage: % recur.py text keyword')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        file = sys.argv[1]
        keyword = sys.argv[2]
        
    occurs = parse (file, keyword)
    print (occurs.reshape((2,2)))
    

if __name__ == "__main__":
    main ()
