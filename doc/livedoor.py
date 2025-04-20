#!/usr/local/bin/python
#
#    livedoor.py
#    parser for the Livedoor News corpus.
#    $Id: livedoor.py,v 1.2 2023/01/31 09:24:25 daichi Exp $
#
import re
import os
import sys
import MeCab
import numpy as np
from os.path import basename
from eprint import eprint,eprintf
from collections import defaultdict
from unicodedata import normalize as unormalize

tagger = MeCab.Tagger('-Owakati')
threshold = 10

def parse (dir, freq):
    data = []
    for file,category in scan (dir):
        eprintf ('parsing %s..\r' % file)
        if re.search (r'LICENSE\.txt', file):
            continue
        doc = docparse (file, category, freq)
        data.append (doc)
    eprint ('parsing done.')
    return data

def docparse (file, category, freq):
    doc = []
    for word in filewords (file):
        if freq[word] >= threshold:
            doc.append (word)
    return doc, category

def preparse (dir):
    freq = defaultdict (int)
    for file,category in scan (dir):
        if re.search (r'LICENSE\.txt', file):
            continue
        eprintf ('reading %s..\r' % file)
        for word in filewords (file):
            freq[word] += 1
    eprint ('preparsing done.')
    return freq

def filewords (file):
    with open (file, 'r') as fh:
        for buf in fh:
            line = unormalize ("NFKC", buf.rstrip('\n'))
            if len(line) > 0:
                if re.search (r'^http://news\.livedoor\.com/', line):
                    continue
                if re.search (r'^\d{4}\-\d{2}\-\d{2}', line):
                    continue
                words = tagger.parse(line).split()
                for word in words:
                    yield word

#
#  I/O functions.
#
                    
def save (data, model):
    eprint ('writing to %s..' % model)
    with open (model, 'w') as oh:
        for datum in data:
            doc = datum[0]
            label = datum[1]
            oh.write ('%s\t%s\n' % (label, ' '.join(doc)))
    eprint ('done.')

#
#  directory reading functions.
#
                    
def listdirs (dir):
    dirs = []
    files = os.scandir (dir)
    for file in files:
        if file.is_dir():
            dirs.append (file.path)
    return sorted (dirs)

def listfiles (dir):
    dirs = []
    files = os.scandir (dir)
    for file in files:
        if file.is_file():
            dirs.append (file.path)
    return sorted (dirs)

def scan (dir):
    categories = listdirs (dir)
    for category in categories:
        for file in listfiles (category):
            yield file, basename(category)

#
#  main
#

def usage ():
    print ('livedoor.py: data extractor for the livedoor corpus.')
    print ('$Id: livedoor.py,v 1.2 2023/01/31 09:24:25 daichi Exp $')
    print ('usage: % livedoor.py dir model')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        dir = sys.argv[1]
        model = sys.argv[2]

    freq = preparse (dir)
    data = parse (dir, freq)
    save (data, model)

if __name__ == "__main__":
    main ()
