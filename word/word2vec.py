#!/usr/local/bin/python
#
#    word2vec.py
#    gensim Word2Vec driver.
#    $Id: word2vec.py,v 1.3 2020/12/16 02:00:50 daichi Exp $
#
import sys
from gensim.models import word2vec

def usage ():
    print ('usage: % word2vec.py K train model')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        K = int(sys.argv[1])
        file = sys.argv[2]
        output = sys.argv[3]
    sys.stderr.write ('computing word2vec from %s.. ' % file)
    sys.stderr.flush ()
    text = word2vec.Text8Corpus (file)
    model = word2vec.Word2Vec (text, size=K, min_count=10, window=10)
    model.wv.save_word2vec_format (output, binary=False)
    sys.stderr.write ('done.\n')

if __name__ == "__main__":
    main ()
