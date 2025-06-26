#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import MeCab

tagger = MeCab.Tagger ('')

def parse (text):
    node = tagger.parseToNode(text)
    words = []
    while node:
        features = node.feature.split(',')
        surface = node.surface
        print (surface)

        node = node.next








def main ():
    with open (sys.argv[1], 'r') as fh:
        for line in fh:
            sent = line.rstrip('\n')
            parse (sent)




if __name__ == "__main__":
    main ()
