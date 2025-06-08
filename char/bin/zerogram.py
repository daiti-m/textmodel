#!/usr/local/bin/python

import sys
from numpy.random import rand

def randchar (chars):
    s = 0
    r = rand()
    p = 1 / len(chars)
    for c in chars:
        s += p
        if (r < s):
            return c
    return c

def gen (chars, L):
    s = ''
    for i in range(L):
        s += randchar (chars)
    return s

def read (file):
    chars = {}
    with open (file, 'r') as f:
        for line in f:
            s = [c for c in line.rstrip('\n')]
            for c in s:
                chars[c] = 1
    return chars

def usage ():
    print ('usage: zerogram.py file N L')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        file = sys.argv[1]
        N = int (sys.argv[2])
        L = int (sys.argv[3])
        
    chars = read (file)
    for n in range(N):
        print (gen(chars, L))

if __name__ == "__main__":
    main ()




    
