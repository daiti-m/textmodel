#!/usr/local/bin/python2
#
#    dirichlet.py
#    drawing a multinomial from Dirichlet distribution.
#    $Id: dirichlet.py,v 1.1 2021/04/26 17:17:38 daichi Exp $
#
import sys
import putil
import numpy as np
from numpy.random import dirichlet
from numpy.random import gamma
from pylab import *

def draw_mult (p):
    K = len(p)
    putil.figaspect (1.2)
    bar (np.arange(K)+0.5, p, width=0.75, align='center', color='black')
    axis([0,K,0,1])
    tick_params (labelsize=28)
    xticks ([])
    tight_layout ()

def sample_dirichlet (alpha):
    p = mydirichlet (alpha)
    # p = dirichlet (alpha)
    draw_mult (p)

def mydirichlet (alpha):
    K = len(alpha)
    gammas = [gamma(alpha[k]) for k in range(K)]
    return np.array (gammas / sum(gammas))

def usage ():
    print ('usage: dirichlet.py alpha K [output]')
    print ('$Id: dirichlet.py,v 1.1 2021/04/26 17:17:38 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    alpha = float (sys.argv[1])
    K     = int (sys.argv[2])
    sample_dirichlet (alpha * np.ones(K))
    if len(sys.argv) > 3:
        savefig (sys.argv[3])
    show ()

if __name__ == "__main__":
    main ()
