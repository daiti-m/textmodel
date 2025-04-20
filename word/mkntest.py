#!/usr/local/bin/python

from collections import defaultdict


def main ():
    xx = [3,2,1,1,5,2,7,1,2,3]
    nc = defaultdict (int)
    nk1 = 0
    nk2 = 0
    nk3 = 0
    
    for x in xx:
        nc[x] += 1
        if nc[x] == 1:
            nk1 += 1
        elif nc[x] == 2:
            nk2 += 1
            nk1 -= 1
        elif nc[x] == 3:
            nk3 += 1
            nk2 -= 1

    print (nk1,nk2,nk3)
    












if __name__ == "__main__":
    main ()
