#!/usr/local/bin/python
#
#    klingon.py
#    parsing Hamlet in Klingon.
#    $Id: klingon.py,v 1.1 2024/04/26 06:57:39 daichi Exp $
#

import re
import sys

def output (text):
    text = re.sub (r'^[a-zA-Z\']+:\s+', '', text)
    text = re.sub (r'^\s+', '', text)
    # print ('text = |%s|' % text)
    sents = list (filter (lambda x: len(x) > 0,
                          re.split (r'(?:\.|\?|\!|---)', text)))
    for sent in sents:
        words = sent.split ()
        clean = []
        if len(words) > 1:
            for word in words:
                clean.append (re.sub (r'[,:;]$', '', word))
            print (' '.join(clean))
            
def parse (file):
    with open (file, "r") as fh:
        text = ""
        intext = False
        for buf in fh:
            line = buf.rstrip('\n')
            if re.search (r'^\[', line):
                intext = True
                continue
            if intext:
                if re.search (r'^\[', line):
                    continue
                line = re.sub (r'\[.+?\]', '', line)
                if len(line) == 0:
                    if len(text) > 0:
                        output (text)
                    text = ""
                else:
                    if text == "":
                        text = line
                    else:
                        text += (" " + line)
            
def usage ():
    print ('usage: % klingon.py klingon-hamlet > output')
    print ('$Id: klingon.py,v 1.1 2024/04/26 06:57:39 daichi Exp $')
    sys.exit (0)
    
def main ():
    if len(sys.argv) < 2:
        usage ()
    parse (sys.argv[1])


if __name__ == "__main__":
    main ()
