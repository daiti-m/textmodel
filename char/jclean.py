#!/usr/local/bin/python

import re
import sys

def main ():
    with open (sys.argv[1], 'r') as fh:
        for buf in fh:
            line = buf.rstrip('\n').lstrip('　')
            print (line)

if __name__ == "__main__":
    main ()
