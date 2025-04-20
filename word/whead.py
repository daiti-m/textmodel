#!/usr/local/bin/python

import sys
from readword import readword

def usage ():
    print ('usage: % whead.py text N > output')
    print ('$Id$')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        text = sys.argv[1]
        N = int (sys.argv[2])
    with open (text, "r") as fh:
        shown = 0
        for word in readword(fh):
            shown += 1
            if (shown >= N):
                print (word)
                break
            else:
                print (word, end=' ')

if __name__ == "__main__":
    main ()
