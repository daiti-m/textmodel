#!/usr/local/bin/python
#
#    bigram.py
#    create SVMlight format for bigram frequencies.
#    $Id: bigram.py,v 1.5 2024/11/14 01:27:55 daichi Exp $
#

import sys
from eprint import eprintf
from collections import defaultdict

EOS = '_EOS_'
UNK = '_UNK_'

def vocabulary (file, threshold=1):
    vocab = {}
    vocab[EOS] = len(vocab) + 1
    vocab[UNK] = len(vocab) + 1
    freq = defaultdict (int)
    # read text
    eprintf ("creating vocabulary..\n")
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            if len(words) > 0:
                for word in words:
                    freq[word] += 1
    # create vocabulary
    for (word,c) in sorted (freq.items(), key=lambda x: x[1],
                            reverse=True):
        if (c >= threshold):
            vocab[word] = len(vocab) + 1
    return vocab

def parse (file, vocab):
    data = {}
    lines = 0
    with open (file, 'r') as fh:
        for line in fh:
            lines += 1
            if (lines % 10000 == 0):
                eprintf ("reading lines %4d..\r" % lines)
            words = line.rstrip('\n').split()
            if len(words) > 0:
                words.insert (0, EOS)
                words.append (EOS)
                T = len(words)
                for t in range(T-1):
                    w = vocab[words[t]] if (words[t] in vocab) else vocab[UNK]
                    v = vocab[words[t+1]] if (words[t+1] in vocab) else vocab[UNK]
                    if not (w in data):
                        data[w] = defaultdict (int)
                    data[w][v] += 1
    eprintf ("reading lines %4d.. done.\n" % lines)
    return data

def write (data, vocab, output):
    eprintf ("writing to %s.{dat,dic}.. " % output)
    write_data (data, output + '.dat')
    write_vocab (vocab, output + '.dic')
    eprintf ("done.\n")

def write_data (data, file):
    with open (file, 'w') as oh:
        for w in data:
            oh.write ('%d\t' % w)
            for (v,c) in data[w].items():
                oh.write ('%d:%d ' % (v,c))
            oh.write ('\n')

def write_vocab (vocab, file):
    with open (file, 'w') as oh:
        for word,id in sorted (vocab.items(), key=lambda x: x[1]):
            oh.write ('%d\t%s\n' % (id, word))

def usage ():
    print ('usage: % bigram.py text threshold output{.dat,.dic}')
    print ('$Id: bigram.py,v 1.5 2024/11/14 01:27:55 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        file = sys.argv[1]
        threshold = int (sys.argv[2])
        output = sys.argv[3]

    vocab = vocabulary (file, threshold)
    data = parse (file, vocab)
    write (data, vocab, output)


if __name__ == "__main__":
    main ()
