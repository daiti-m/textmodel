#!/bin/env python
#
#    util.py
#    private utilities for Python.
#    $Id: util.py,v 1.7 2023/02/14 02:37:27 daichi Exp $
#
import numpy as np
from numpy.linalg import norm
from unicodedata import east_asian_width
from pylab import *

#
#  string functions
#

def char_width (c):
    t = east_asian_width (c)
    if t == "F":
        return 2
    elif t == "H":
        return 1
    elif t == "W":
        return 2
    elif t == "Na":
        return 1
    else:
        return 1

def ulen (s):
    l = 0
    for c in s:
        l += char_width (c)
    return l

def usubstr (s, length):
    x = ''
    l = 0
    for c in s:
        l += char_width (c)
        x += c
        if not (l < length):
            return x
    return s

def utruncate (s, length):
    x = ''
    l = 0
    for c in s:
        l += char_width (c)
        x += c
        if not (l < length):
            return x + '..'
    return s

# return numpy array from str(v) = '[1 10 23]'

def npstr (s):
    return np.fromstring (s[1:-1], dtype=float, sep=' ')

def npstri (s):
    return np.fromstring (s[1:-1], dtype=int, sep=' ')

def converged (u,v,eps=1e-4):
    return (norm(u - v) / norm(u) < eps)

def savetxt (file, var):
    np.savetxt (file, var, fmt='% .7f')

def vload(file):
    n = filelines (file)
    v = np.zeros (n)
    i = 0
    with open(file, 'r') as fh:
        for buf in fh:
            v[i] = float(buf)
            i = i + 1
    return v

def mload(file):
    return np.loadtxt(file)

def sload(file):
    with open(file) as fh:
        data = fh.read()
    words = data.split('\n')
    if words[-1] == '':
        words.pop()
    return words

def filelines (file):
    n = 0
    with open(file, 'r') as fh:
        n = len(fh.readlines())
    return n

#
#  list/vector
#

def divide (n, xx):  # more_itertools.divide is not convenient
    N = len (xx)
    L = int (N / n)
    return [ (xx[L*i:L*(i+1)] if i < n-1 else xx[L*i:]) for i in range(n)]

def flatten (xx):
    result = []
    for x in xx:
        result += x
    return result
