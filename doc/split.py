#!/usr/local/bin/python
#
#    split.py
#    $Id: split.py,v 1.1 2023/01/31 09:35:54 daichi Exp $
#
import sys
import random
from util import divide, flatten

def save (data, index, file):
    with open (file, 'w') as oh:
        for n in index:
            oh.write (data[n] + '\n')
            
def load (file):
    data = []
    with open (file, 'r') as fh:
        for line in fh:
            data.append (line.rstrip('\n'))
    return data

def usage ():
    print ('usage: % split.py data output [N]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
        
    data = load (sys.argv[1])
    output = sys.argv[2]
    N = len (data)
    n = int (sys.argv[3]) if len(sys.argv) > 3 else 10
    index = list (range(N))

    random.shuffle (index)
    splits = divide (n, index)
    
    train = flatten (splits[:-2])
    dev   = splits[-2]
    test  = splits[-1]

    #
    #  output
    #
    save (data, train, output + '.train')
    save (data, dev,   output + '.dev')
    save (data, test,  output + '.test')



if __name__ == "__main__":
    main ()
