#!/usr/local/bin/python

import re
import sys

def main ():
    s = 0
    with open (sys.argv[1], 'r') as fh:
        for buf in fh:
            line = buf.rstrip('\n').lstrip('　')
            s += len(line)
    print (s)

if __name__ == "__main__":
    main ()
