#!/bin/env python
#
#    eprint.py
#    stderr printing function.
#    $Id: eprint.py,v 1.2 2020/04/02 13:38:31 daichi Exp $
#
import sys

esc = '\x1b[K'

def cls ():
    sys.stderr.write (esc)

def eprint (s,clear=True):
    if clear:
        cls ()
    sys.stderr.write (s + "\n")
    sys.stderr.flush ()
        
def eprintf (s,clear=True):
    if clear:
        cls ()
    sys.stderr.write (s)
    sys.stderr.flush ()
