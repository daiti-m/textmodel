#!/usr/local/bin/python
#
#    article-id.py
#    $Id: article-id.py,v 1.3 2024/04/17 02:21:38 daichi Exp $
#
import re
import sys
import random
import numpy as np

def parse (file, name, ndocs):
    pos = []
    lines = 0
    with open (file, "r") as fh:
        for line in fh:
            label = line.rstrip('\n')
            lines += 1	# 1-based indexing for R
            if re.search (name, label):
                pos.append (lines)
    # print
    if (not (ndocs > 0)) or (len(pos) <= ndocs):
        print (','.join(map(str,pos)))
    else:
        random.shuffle (pos)
        print (','.join(map(str,sorted(pos[0:ndocs]))))

def usage ():
    print ("usage: % article-id.py data.label name [N]")
    print ("$Id: article-id.py,v 1.3 2024/04/17 02:21:38 daichi Exp $")
    sys.exit (0);

def main ():
    if len(sys.argv) < 3:
        usage ();
    file = sys.argv[1]
    name = sys.argv[2]
    ndocs = int (sys.argv[3]) if len(sys.argv) > 3 else 0

    parse (file, name, ndocs)


if __name__ == "__main__":
    main ()
