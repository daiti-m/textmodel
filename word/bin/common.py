#!/usr/local/bin/python

import sys

def common (words1, words2):
    dic = {}
    result = []
    for word in words1:
        dic[word] = 1
    for word in words2:
        if (word in dic):
            result.append (word)
    return result

def loadtxt (file):
    with open (file, 'r') as fh:
        words = fh.read().split('\n')[0:-1]
    return words

def usage ():
    print ('usage: % common.py text1 text2')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    words1 = loadtxt (sys.argv[1])
    words2 = loadtxt (sys.argv[2])
    # print ('  '.join(common (words1, words2)))
    for word in common(words1, words2):
        print (word)


if __name__ == "__main__":
    main ()
