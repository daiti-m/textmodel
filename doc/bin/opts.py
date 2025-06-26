#!/usr/local/bin/python
#
#    opts.py
#    $Id: opts.py,v 1.4 2019/03/17 01:21:37 daichi Exp $
#
import re
import sys
import getopt

def optchar (s):
    if s[-1] == '=':
        s = s[0:-1]
    if s[0:2] == '--':
        return s[2:]
    elif s[0] == '-':
        return s[1:]
    else:
        return s

def getopts (directive):
    dic   = {}
    chars = []
    longs = []
    short = ''
    # parse directives
    for item in directive:
        # option key
        [char,long] = item.split('|')
        if re.search(r'=$', long):
            short += ('%s:' % char)
        else:
            short += char
        chars.append (char)
        longs.append (long)
    # analyze argv
    try:
        opts,args = getopt.getopt (sys.argv[1:], short, longs)
    except getopt.GetoptError as err:
        usage ()
    # register dictionary
    for o,a in opts:
        oo = optchar (o)
        for char,long in zip (chars, longs):
            long = (long[0:-1] if long[-1] == '=' else long)
            if oo in (char, long):
                dic[char] = (True if a == '' else a)
                break
    return dic, args

def getopts1 (optarray):
    chars = []
    longs = []
    short = ''
    # parse directives
    for item in optarray:
        [char,long] = item.split('|')
        if re.search(r'=$', long):
            short += ('%s:' % char)
        else:
            short += char
        chars.append (char)
        longs.append (long)
    # analyze argv
    try:
        opts,args = getopt.getopt (sys.argv[1:], short, longs)
    except getopt.GetoptError as err:
        usage ()
    # create dictionary
    dic = {}
    for o,a in opts:
        oo = optchar (o)
        for char,long in zip (chars, longs):
            long = (long[0:-1] if long[-1] == '=' else long)
            if oo in (char, long):
                dic[char] = (None if a == '' else a)
                break
    return dic,args

# for test
# 
# def main ():
#     # opts,args = getopts ({"L|latents=":2, "f|foo=":"bar", "h|help":None})
#     opts,args = getopts (["L|latents=", "f|foo=", "h|help"])
#     print (opts)
#     print (args)
#     if 'h' in opts:
#         print ('HELP!')
# 
# def usage ():
#     print ('usage: opts.py [-L latents] [-f arg] [-h] train model')
#     sys.exit (0)
# 
# if __name__ == "__main__":
#     main ()
