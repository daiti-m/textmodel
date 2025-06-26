#!/usr/local/bin/python

import sys
import csv
import MeCab
import numpy as np
from neologdn import normalize

tagger = MeCab.Tagger('-Owakati')

def words (text):
    results = []
    for sent in text.split('\n'):
        results.extend (tagger.parse(sent).split())
    return results

def parse (file):
    with open (file, "r") as fh:
        lines = 0
        for cols in csv.reader(fh, delimiter='\t'):
            if lines > 0:
                text = normalize (cols[0], repeat=3)
                body = ' '.join (words(text))
                polarity = int (cols[12])
                # if (abs(polarity) > 1):
                #     print ('%d\t%s' % (polarity, body))
                if (polarity > 1):
                    print ('positive\t%s' % body)
                if (polarity < -1):
                    print ('negative\t%s' % body)
            lines += 1

def usage ():
    print ('usage: % wrime.py wrime.tsv > output')
    print ('$Id: wrime.py,v 1.2 2024/04/06 01:47:13 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()

    parse (sys.argv[1])


if __name__ == "__main__":
    main ()
