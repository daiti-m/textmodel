#!/usr/local/bin/python
# -*- utf-8 -*-

import sys
import regex
import numpy as np

def ctype (c):
    if (c == "ー") or (c == "ﾞ") or (c == "ｰ"):
        # exception
        return 'Katakana'
    elif (c == " ") or (c == "　"):
        return 'Punct'
    elif is_latin (c):
        return 'Latin'
    elif is_kanji (c):
        return 'Kanji'
    elif is_hiragana (c):
        return 'Hiragana'
    elif is_katakana (c):
        return 'Katakana'
    elif is_numeric (c):
        return 'Numeric'
    elif is_punct (c):
        return 'Punct'
    elif is_emoji (c):
        return 'Emoji'
    else:
        return 'Others'

def is_latin (c):
    return regex.match(r'\p{Latin}$', c)
    
def is_kanji (c):
    return regex.match(r'\p{Han}+$', c)
    
def is_hiragana (c):
    return regex.match(r'\p{Hiragana}+$', c)

def is_katakana (c):
    return regex.match(r'\p{Katakana}+$', c)

def is_numeric (c):
    return regex.match(r'[0-9０-９]+$', c)

def is_punct (c):
    return regex.match(r'\p{Punctuation}$', c)

def is_emoji (c):
    return regex.match(r'\p{Emoji=Yes}$', c)

    
def main ():
    with open (sys.argv[1], 'r') as fh:
        for line in fh:
            chars = [c for c in line.rstrip('\n')]
            ctypes = [ctype(c) for c in chars]
            T = len(chars)
            for t in range(T):
                print ('%s\t%s' % (chars[t], ctype(chars[t])))
            # print ("-----")


if __name__ == "__main__":
    main ()
