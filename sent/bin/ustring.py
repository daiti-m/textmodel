#!/usr/local/bin/python
#
#    ustring.py
#    unicode string utility.
#    $Id: ustring.py,v 1.1 2024/02/23 06:51:17 daichi Exp $
#

import sys
from unicodedata import east_asian_width

def ulength (s):
    l = 0
    for c in s:
        if east_asian_width(c) in 'FWA':
            l += 2
        else:
            l += 1
    return l



def main ():
    s = sys.argv[1]
    print ('length of |%s| = %d' % (s, ulength(s)))


if __name__ == "__main__":
    main ()
