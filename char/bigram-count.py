#!/usr/local/bin/python

import sys
from collections import defaultdict

freq = defaultdict (int)

with open (sys.argv[1], 'r') as fh:
    for buf in fh:
        s = buf.rstrip('\n')
        N = len(s)
        s += '$'
        for i in range(N):
            b = s[i:i+2]
            freq[b] += 1
            
for (b,n) in freq.items():
    print ('%s = %d' % (b, n))
print ('total %d bigrams.' % sum(freq.values()))
