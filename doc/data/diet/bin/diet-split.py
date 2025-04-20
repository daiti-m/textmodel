#!/usr/local/bin/python

import re
import sys

def parse (fh):
    header = 1;
    for line in fh:
        if re.search (r'^○', line):
            header = 0
            person = None
            print ('')
        if (header == 1):
            continue
        if re.search (r'[　 ]*[─―◇]+[　 ]*$', line):
            continue
        cline = line.rstrip('\n')
        if re.search (r'^○', line):
            tokens = cline.split('　')
            if len(tokens) > 1:
                person = tokens[0]
                content = '　'.join (tokens[1:])
                print (person)
                print (content)
        else:
            if person is not None:
                print (cline)
        

def main ():
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            with open (file, 'r') as fh:
                parse (fh)
    else:
        parse (sys.stdin)

if __name__ == "__main__":
    main ()
