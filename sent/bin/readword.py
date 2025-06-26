#!/usr/local/bin/python
#
#    readword.py
#    to read off words from very long line of text.
#    $Id: readword.py,v 1.4 2022/08/25 01:03:23 daichi Exp $
#
import re

def readword (fh, newline=r'[ \t\n]+'):
    buf = ""
    while True:
        while True:
            match = re.search (newline, buf)
            if not match:
                break
            else:
                yield buf[:match.start()]
                buf = buf[match.end():]
        chunk = fh.read (4096)
        if not chunk:
            if len(buf) > 0:
                yield buf
            break
        buf += chunk

def main ():
    with open (sys.argv[1], "r") as fh:
        for word in readword(fh, r'[ \n]+'):
            print (word)

if __name__ == "__main__":
    import sys
    main ()
