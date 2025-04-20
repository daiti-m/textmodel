#!/usr/local/bin/python

import sys
import gzip
import pickle
import numpy as np
from itertools import combinations
from collections import defaultdict
from pylab import *

def coherence (topicwords, unigram, bigram):
    K = len(topicwords)
    result = np.zeros (K, dtype=float)
    for k in range(K):
        result[k] = topic_coherence (topicwords[k], unigram, bigram)
        # print ('coherence[%d] = %.4f' % (k+1, result[k]))
    print ('average = %.4f' % np.mean (result))

def topic_coherence (words, unigram, bigram):
    s = 0; n = 0
    for word1,word2 in combinations (words, 2):
        s += npmi (word1, word2, unigram, bigram)
        n += 1
    return s / n

def npmi (word, cword, unigram, bigram):
    if not (cword in unigram):
        return 0
    if not (cword in bigram[word]):
        return 0
    return 1 - (log (bigram[word][cword]) / log (unigram[cword]))

def cooccur (topicwords, corpus, width):
    lexicon = union (topicwords)
    unigram = defaultdict (int)
    bigram  = {}
    for word in lexicon:
        bigram[word] = defaultdict (int)
    with open (corpus, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            if len(words) > 0:
                T = len(words)
                for t in range(T):
                    word = words[t]
                    if (word in lexicon):
                        unigram[word] += 1
                        for cword in window (words, t, width):
                            if cword in lexicon:
                                bigram[word][cword] += 1
    # normalize
    Z = sum (list (unigram.values()))
    for word,count in unigram.items():
        unigram[word] = count / Z
    for word in bigram.keys():
        Z = sum (list (bigram[word].values()))
        for cword,count in bigram[word].items():
            bigram[word][cword] = count / Z
    return unigram, bigram

def union (topicwords):
    lexicon = set()
    for words in topicwords:
        lexicon |= words
    return lexicon

def window (words, t, width):
    st = t - width
    ed = t + width
    if (st < 0):
        st = 0
    if (ed > len(words) - 1):
        ed = len(words) - 1
    return words[st:t] + words[t+1:ed+1]

def topwords (model, top=10):
    K,V = model['beta'].T.shape
    beta = model['beta'].T
    lexicon = tolexicon (model)
    topicwords = [set() for k in range(K)]
    for k in range(K):
        seen = 0
        for p,word in sorted (zip(beta[k], lexicon), key=lambda x: x[0], reverse=True):
            topicwords[k].add (word)
            seen += 1
            if (seen >= top):
                break
    return topicwords

def tolexicon (model):
    dic = {}
    if 'lexicon' in model:
        lexicon = model['lexicon']
    elif 'vocab' in model:
        lexicon = model['vocab']
    else:
        print ('lexicon does not exist in the model.')
        sys.exit (1)
    for word,id in lexicon.items():
        dic[id] = word
    V = model['beta'].shape[0]
    return [(dic[v] if v in dic else "") for v in range(V)]

def load (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % coherence.py model corpus.txt [window] [top]')
    print ('$Id: coherence.py,v 1.3 2023/06/14 01:18:54 daichi Exp $')
    sys.exit (0)


def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        model = load (sys.argv[1])
        corpus = sys.argv[2]
        window = int (sys.argv[3]) if len(sys.argv) > 3 else 10
        top    = int (sys.argv[4]) if len(sys.argv) > 4 else 10
        
    print ('obtaining topic words..')
    topicwords = topwords (model, top)
    print ('computing cooccurrences..')
    unigram,bigram = cooccur (topicwords, corpus, window)
    print ('calculating coherence..')
    coherence (topicwords, unigram, bigram)



if __name__ == "__main__":
    main ()
