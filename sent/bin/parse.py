#!/usr/local/bin/python

import sys
from nltk.parse import CoreNLPParser
from nltk.draw.tree import TreeView

def parse (s):
    parser = CoreNLPParser (url='http://localhost:9000')
    return list(parser.raw_parse(s))[0][0]

def save (t, file):
    TreeView(t)._cframe.print_to_file (file)


def main ():
    t = parse (sys.argv[1])
    save (t, sys.argv[2])


if __name__ == "__main__":
    main ()
