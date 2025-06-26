#!/usr/local/bin/python

import sys
from nltk.tree import Tree
from nltk.draw.tree import TreeView

def save (t, file):
    TreeView(t)._cframe.print_to_file (file)

def main ():
    t = Tree.fromstring (sys.argv[1])
    save (t, sys.argv[2])


if __name__ == "__main__":
    main ()
