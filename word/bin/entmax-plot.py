#!/usr/local/bin/python

import sys
import putil
import torch
import numpy as np
from torch.nn.functional import softmax
from entmax import sparsemax, entmax15, entmax_bisect
from pylab import *

# x = torch.tensor ([-4,-3,-2,0,1,2.0])
x = torch.tensor ([-3,-2,0,1,2.0])
y = softmax (x, dim=0)
y2 = entmax15 (x, dim=0)
K = len(x)

figure (figsize=(8,2.2))
subplots_adjust (wspace=0.33)

subplot(1,2,1)
bar (range(K), y)
ylim (0,1)
xticks (np.arange(0,K))
yticks (np.arange(0,1.25,0.25))
putil.xticklabels (range(1,K+1))
subplot(1,2,2)
bar (range(K), y2)
ylim (0,1)
xticks (np.arange(0,K))
yticks (np.arange(0,1.25,0.25))
putil.xticklabels (range(1,K+1))

if len(sys.argv) > 1:
    putil.savefig (sys.argv[1], dpi=300)
show ()
