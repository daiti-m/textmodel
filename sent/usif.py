#!/usr/local/bin/python
#
#    usif.py
#    uSIF sentence embedding of Ethayarajh (2018).
#    $Id: usif.py,v 1.1 2023/04/27 12:40:08 daichi Exp $
#
import re
import sys
import numpy as np
from eprint import eprintf
from readword import readword
from collections import defaultdict
from pylab import *

class uSIF:
    def __init__ (self, wordvec, wordtxt, sents):
        self.wordvec = loadvec (wordvec)
        self.p = wordprob (wordtxt)
        #
        #  prepare parameters
        #
        L = mean (list (map (len, sents)))
        V = len(self.p)
        threshold = 1 - (1 - 1 / V)**L
        alpha = len ([v for v in self.p.keys() if self.p[v] > threshold]) / V
        a = (1 - alpha) / (alpha * V / 2)
        self.weight = lambda v: (a / (self.p[v] + a / 2))
        
    def embed (self, sent):
        words = [word for word in sent if (word in self.p) and (word in self.wordvec)]
        vectors = [self.wordvec[word] for word in words]
        vectors = [self.weight(word) * normalize(self.wordvec[word]) for word in words]
        # below are the same as Ethayarajh (2018), but performs worse.
        # vectors = vectors / np.linalg.norm (vectors, axis=0)
        # vectors = [self.weight(word) * vectors[i] for i,word in enumerate (words)]
        return np.mean (vectors, axis=0)

    def embeds (self, sents):
        result = []
        for sent in sents:
            result.append (self.embed (sent))
        return results

#
#  supporting functions.
#

def wordprob (file):
    if re.search (r'\.p$', file):
        return loadp (file)
    else:
        return unigram (file)

def loadp (file):
    eprintf ('loading word probabilities from "%s".. ' % file)
    p = {}
    with open (file, 'r') as fh:
        for line in fh:
            tokens = line.rstrip('\n').split('\t')
            if not (len(tokens) == 2):
                print ('error! invalid line.')
                sys.exit (1)
            else:
                word = tokens[0]
                prob = float (tokens[1])
                p[word] = prob
    eprintf ('done.\n', clear=False)
    return p

def unigram (file):
    freq = defaultdict (int)
    p = {}
    N = 0
    with open (file, "r") as fh:
        for word in readword(fh):
            freq[word] += 1
            N += 1
            if (N % 1000000 == 0):
                eprintf ("reading from \"%s\" %s words.. \r" % (file, N))
    eprintf ("reading from \"%s\" %s words.. done.\n" % (file, N))
    for word in freq.keys():
        p[word] = freq[word] / N
    return p

def loadtxt (file):
    data = []
    with open (file, 'r') as fh:
        for line in fh:
            sent = line.rstrip('\n').split()
            data.append (sent)
    return data
    
def loadvec (file):
    eprintf ('loading from "%s".. ' % file)
    vectors = {}
    with open (file, 'r') as fh:
        for line in fh:
            tokens = line.rstrip('\n').split()
            if len(tokens) > 2: # possibly skip word2vec header
                word = tokens[0]
                vectors[word] = np.array (list (map (float, tokens[1:])))
    eprintf ('done.\n')
    return vectors

def save (file, embedder, sents):
    matrix = np.array ([embedder.embed(sent) for sent in sents])
    print ('writing to %s..' % file)
    np.savetxt (file, matrix, fmt='% .7f')
    print ('done.')

def normalize (v):
    return v / norm(v)

def norm (v):
    return np.sqrt (np.dot (v,v))

def comma (n):
    return "{:,}".format (n)

def usage ():
    print ('usif.py: uSIF sentence embedding.')
    print ('usage: % usif.py words.vec words.{txt|p} sentences.txt [output]')
    print ('$Id: usif.py,v 1.1 2023/04/27 12:40:08 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        wordvec = sys.argv[1]
        wordtxt = sys.argv[2]
        sents = loadtxt (sys.argv[3])

    embedder = uSIF (wordvec, wordtxt, sents)

    if len(sys.argv) > 4:
        save (sys.argv[4], embedder, sents)
    else:
        for sent in sents:
            print (embedder.embed (sent))

if __name__ == "__main__":
    main ()
