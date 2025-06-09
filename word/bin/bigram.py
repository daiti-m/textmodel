#!/usr/local/bin/python

import sys
from eprint import eprintf
from collections import defaultdict

wordid = defaultdict (lambda: 1+len(wordid))

def parse (file):
    data = {}
    lines = 0
    with open (file, 'r') as fh:
        for line in fh:
            lines += 1
            if (lines % 1000 == 0):
                eprintf ("reading lines %4d..\r" % lines)
            words = line.rstrip('\n').split()
            if len(words) > 0:
                words.insert (0, '_EOS_')
                words.append ('_EOS_')
                T = len(words)
                for t in range(T-1):
                    w = words[t]
                    v = words[t+1]
                    if not (w in data):
                        data[w] = defaultdict (int)
                    data[w][v] += 1
    eprintf ("reading lines %4d.. done.\n" % lines)
    return data

def write (data, output):
    write_data (data, output + '.dat')
    write_dict (wordid, output + '.dic')

def write_data (data, file):
    with open (file, 'w') as oh:
        for w in data:
            oh.write ('%d\t' % wordid[w])
            for (v,c) in data[w].items():
                oh.write ('%d:%d ' % (wordid[v], c))
            oh.write ('\n')

def write_dict (dic, file):
    with open (file, 'w') as oh:
        for v,id in sorted (dic.items(), key=lambda x: x[1]):
            oh.write ('%d\t%s\n' % (id, v))

def usage ():
    print ('usage: % bigram.py text output{.dat,.dic}')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        file = sys.argv[1]
        output = sys.argv[2]

    data = parse (file)
    write (data, output)


if __name__ == "__main__":
    main ()
