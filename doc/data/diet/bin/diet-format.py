#!/usr/local/bin/python

import re
import sys

def parse (fh):
    person = None
    for line in fh:
        line = line.rstrip('\n')
        if re.search (r'^○', line):
            person = re.sub(r'^○', '', line)
            print (person, end='\t')
            continue
        if person is not None:
            print (line, end='')
        if re.search (r'^$', line):
            person = None
            print ('')

def main ():
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            with open (file, 'r') as fh:
                parse (fh)
    else:
        parse (sys.stdin)

if __name__ == "__main__":
    main ()
