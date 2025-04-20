#!/usr/local/bin/python
"""
fmatrix.py : loading sparse feature matrix.
$Id: fmatrix.py,v 1.1 2020/09/15 12:15:56 daichi Exp $
"""
import numpy as np
import sys

class document:
    def __init__ (self):
        self.id  = []
        self.cnt = []

def parse (file, offset=0):
    data = []
    with open (file, 'r') as fh:
        for line in fh:
            label,content = line.split ('\t')
            tokens = content.split()
            doc = document()
            for token in tokens:
                id,cnt = token.split(':')
                doc.id.append (int(id) - offset)
                doc.cnt.append (int(cnt))
            data.append (doc)
    return data

def plain (file):
    """
    build a plain word sequence for LDA.
    """
    data = []
    with open (file, 'r') as fh:
        for line in fh:
            words = expand (line)
            if len(words) > 0:
                data.append (words)
    return data

def expand (line):
    words = []
    tokens = line.split()
    if len(tokens) > 0:
        for token in tokens:
            [id,cnt] = token.split(':')
            w = int(id)
            c = int(cnt)
            words.extend ([w for x in xrange(c)])
        return words
    else:
        return []

def main ():
    data = plain (sys.argv[1])
    print (data)
    
if __name__ == "__main__":
    main ()
    
