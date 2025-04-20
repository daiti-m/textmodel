#!/usr/local/bin/python
#
#    livedoor2data.py
#    parse Livedoor texts into a SVMlight format.
#    $Id: livedoor2data.py,v 1.2 2023/02/11 03:09:38 daichi Exp $
#

import re
import sys
import regex
import numpy as np
from eprint import eprintf
from collections import defaultdict

def save_data (file, input, dic):
    eprintf ('writing data to %s.. ' % file)
    with open (file, 'w') as oh:
        with open (input, 'r') as fh:
            doc = 0
            for line in fh:
                doc += 1
                label,text = line.rstrip('\n').split('\t')
                words = text.split()
                freq = defaultdict (int)
                for word in words:
                    word = re.sub (r'[0-9]', '#', word)
                    if (word in dic):
                        id = dic[word]
                        freq[id] += 1
                if len(freq) > 0:
                    first = True
                    for id,count in sorted (freq.items(), key=lambda x: x[1],
                                            reverse=True):
                        oh.write ('%s%d:%d' % (('' if first else ' '), id, count))
                        first = False
                    oh.write ('\n')
                else:
                    eprintf ('document %d is empty!!\n' % doc)
    eprintf ('done.\n', clear=False)                    

def save_dic (file, dic):
    eprintf ('writing dic to %s.. ' % file)
    with open (file, 'w') as oh:
        for word,id in sorted (dic.items(), key=lambda x: x[1]):
            oh.write ('%d\t%s\n' % (id, word))
    eprintf ('done.\n', clear=False)

def parse (file, dic, output):
    save_dic (output + '.lex', dic)
    save_data (output + '.dat', file, dic)

def vocabulary (file, threshold):
    freq = defaultdict (int)
    dic = {}
    id = 0
    # parse
    with open (file, 'r') as fh:
        for line in fh:
            label,text = line.rstrip('\n').split('\t')
            words = text.split()
            for word in words:
                word = re.sub (r'[0-9]', '#', word)
                freq[word] += 1
    # register
    for word,count in sorted (freq.items(), key=lambda x: x[1], reverse=True):
        if (count >= threshold) and isvalid(word):
            id += 1
            dic[word] = id
    return dic

def isvalid (s):
    if regex.search (r'^\p{Hiragana}+$', s):
        return False
    else:
        return regex.search (r'(\p{Han}|\p{Hiragana}|\p{Katakana}|\p{alnum})', s)

def usage ():
    print ('usage: % livedoor2data.py train.txt output{.dat,lex} [threshold]')
    print ('$Id: livedoor2data.py,v 1.2 2023/02/11 03:09:38 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        text = sys.argv[1]
        output = sys.argv[2]
        threshold = int (sys.argv[3]) if len(sys.argv) > 3 else 10

    dic = vocabulary (text, threshold)
    parse (text, dic, output)


if __name__ == "__main__":
    main ()
