#!/usr/local/bin/python
#
#    HMM.py
#    Bayesian hidden Markov model module.
#    $Id: hmm.py,v 1.1 2023/05/13 23:35:41 daichi Exp $
#
import sys
import loggings
import numpy as np
from loggings import elprintf
from numpy import log,exp,sum
from scipy.special import gammaln
from numpy.random import rand,randn,randint
from numpy.random import permutation as randperm
from rutil import multinom, pmultinom, lmultinom

def learn (data, K, gamma, eta, iters, model):
    loggings.start (sys.argv, model)
    # initialize
    N = len (data)
    V = lexicon (data)
    zz = [[] for n in range(N)]
    nz = np.zeros (K+1)
    nzz = np.zeros ((K+1,K+1))
    nzw = np.zeros ((K+1,V))
    # MCMC
    for iter in range(iters):
        for n in randperm(N):
            if iter > 0:
                remove_counts (data[n], zz[n], nzz, nzw, nz)
            zz[n] = ffbs (data[n], nzz, nzw, nz, gamma, eta)
            add_counts (data[n], zz[n], nzz, nzw, nz)
        elprintf ('iter[%2d]: PPL = %.02f' % \
                  (iter+1, perplexity (data,nz,nzz,nzw,gamma,eta)))
    eprintf('\n')

    # model
    model = convert_model (zz,nz,nzz,nzw,gamma,eta)
    loggings.finish ()
    return model

def ffbs (words, nzz, nzw, nz, gamma, eta):
    # forward filtering, backward sampling in HMM.
    K = nzw.shape[0] - 1
    V = nzw.shape[1]
    T = len (words)
    zz = np.zeros (T,dtype=int)
    alpha = np.zeros ((T,K))
    # initialize
    for k in range(K):
        alpha[0][k] = log ((nzz[K][k] + gamma) / (nz[K] + gamma * K) * \
                           (nzw[k][words[0]] + eta) / (nz[k] + eta * V))
    # forward filtering
    for t in range(1,T):
        w = words[t]
        for k in range(K):
            p = (nzw[k][w] + eta) / (nz[k] + V * eta)
            qs = (nzz[0:K,k] + gamma) / (nz[0:K] + gamma * (K+1))
            alpha[t][k] = log(p) + logsumexp (alpha[t-1] + log(qs))
    # backward sampling
    qs = (nzz[0:K,K] + gamma) / (nz[0:K] + gamma * (K+1))
    zz[T-1] = lmultinom (alpha[T-1] + log(qs))
    for t in range(T-2,-1,-1):
        qs = (nzz[0:K,zz[t+1]] + gamma) / (nz[0:K] + gamma * (K+1))
        zz[t] = lmultinom (alpha[t] + log(qs))
        
    return zz

def add_counts (words, zz, nzz, nzw, nz):
    T = len (words)
    K = nzz.shape[0] - 1
    for t in range(T):
        nz[zz[t]] += 1
        nzw[zz[t]][words[t]] += 1
        if (t < T - 1):
            nzz[zz[t]][zz[t+1]] += 1
    # BOS/EOS
    nz[K] += 1
    nzz[K][zz[0]] += 1
    nzz[zz[T-1]][K] += 1

def remove_counts (words, zz, nzz, nzw, nz):
    T = len (words)
    K = nzz.shape[0] - 1
    for t in range(T):
        nz[zz[t]] -= 1
        nzw[zz[t]][words[t]] -= 1
        if (t < T - 1):
            nzz[zz[t]][zz[t+1]] -= 1
    # BOS/EOS
    nz[K] -= 1
    nzz[K][zz[0]] -= 1
    nzz[zz[T-1]][K] -= 1

#
#  Gibbs sampling (no dynamic programming)
#

def gibbs (data, K, gamma, eta, iters, model):
    loggings.start (sys.argv, model)
    # initialize
    N = len (data)
    V = lexicon (data)
    zz = [[randint(K) for i in range(len(data[n]))] for n in range(N)]
    nz = np.zeros (K+1)
    nzz = np.zeros ((K+1,K+1))
    nzw = np.zeros ((K+1,V))
    # initialization
    for n in range(N):
        T = len(data[n])
        for t in range(T):
            add_count (t, data[n], zz[n], nzz, nzw, nz, initial=True)
    # Gibbs sampler
    for iter in range(iters):
        for n in randperm(N):
            T = len(data[n])
            for t in randperm(T):
                remove_count (t, data[n], zz[n], nzz, nzw, nz)
                zz[n][t] = draw_gibbs (t, data[n], zz[n], nzz, nzw, nz, gamma, eta)
                add_count (t, data[n], zz[n], nzz, nzw, nz)
        elprintf ('iter[%2d]: PPL = %.02f' % \
                  (iter+1, perplexity (data,nz,nzz,nzw,gamma,eta)))
    eprintf ('\n')
    # model
    model = convert_model (zz,nz,nzz,nzw,gamma,eta)
    loggings.finish ()
    return model

def draw_gibbs (t, words, zz, nzz, nzw, nz, gamma, eta):
    z = zz[t]
    w = words[t]
    T = len(words)
    V = nzw.shape[1]
    K = nzz.shape[0] - 1
    buf = np.zeros (K, dtype=float)
    # compute probabilities
    pz = zz[t-1] if t > 0 else K
    qz = zz[t+1] if t < T-1 else K
    for z in range(K):
        p = (nzz[pz][z] + gamma) / (nz[pz] + gamma * (K+1))
        if (pz == z) and (z == qz):
            q = (nzz[z][qz] + 1 + gamma) / (nz[z] + 1 + gamma * (K+1))
        else:
            q = (nzz[z][qz] + gamma) / (nz[z] + gamma * (K+1))
        r = (nzw[z][w] + eta) / (nz[z] + V * eta)
        buf[z] = p * q * r
    return pmultinom (buf)

def remove_count (t, words, zz, nzz, nzw, nz):
    z = zz[t]
    w = words[t]
    T = len(words)
    K = nzz.shape[0] - 1
    # observations
    nzw[z][w] -= 1
    # total counts
    nz[z] -= 1
    # transitions
    if t > 0:
        nzz[zz[t-1]][z] -= 1
    else:
        nzz[K][z] -= 1
    if t < T-1:
        nzz[z][zz[t+1]] -= 1
    else:
        nzz[z][K] -= 1
        nz[K] -= 1
    
def add_count (t, words, zz, nzz, nzw, nz, initial=False):
    z = zz[t]
    w = words[t]
    T = len(words)
    K = nzz.shape[0] - 1
    # observations
    nzw[z][w] += 1
    # total counts
    nz[z] += 1
    # transitions
    if t > 0:
        nzz[zz[t-1]][z] += 1
    else:
        nzz[K][z] += 1
    if t < T-1:
        if not initial:
            nzz[z][zz[t+1]] += 1
    else:
        nzz[z][K] += 1
        nz[K] += 1
        
# likelihood computation

def hmmlik (nz,nzz,nzw,alpha,eta):
    return hmmlik_nzz (nzz,alpha) + hmmlik_nzw (nzw,eta)

def hmmlik_nzz (nzz,alpha):
    K = nzz.shape[0] - 1
    lik = polya_lik (nzz[K,:],alpha,K)
    for k in range(K):
        lik += polya_lik (nzz[k,:],alpha,K+1)
    return lik

def hmmlik_nzw (nzw,eta):
    K = nzw.shape[0] - 1
    V = nzw.shape[1]
    lik = 0
    for k in range(K):
        lik += polya_lik (nzw[k,:],eta,V)
    return lik

def polya_lik (xx,alpha,K):
    lik = gammaln (alpha * K) - gammaln (alpha * K + sum(xx))
    lik += sum (gammaln (xx + alpha) - gammaln (alpha))
    return lik

def perplexity (data,nz,nzz,nzw,gamma,eta):
    L = sum (list (map (len, data)))
    lik = hmmlik (nz,nzz,nzw,gamma,eta)
    return exp (- lik / L)

# supporting functions

def lexicon (data):
    return max (list (map (max, data))) + 1

def lmultinom (lik):
    theta = exp (lik - logsumexp(lik))
    return multinom (theta)

def logsumexp (x):
    y = max (x)
    return y + log(sum(exp(x - y)))

def convert_model (zz,nz,nzz,nzw,gamma,eta):
    model = {}
    model['zz']    = zz
    model['trans'] = rnormalize (nzz + gamma)
    model['emit']  = rnormalize (nzw[:-1,:] + eta)
    return model

def rnormalize (M): # row-wise normalize matrix
    return np.array ([m / np.sum(m) for m in M])

def eprint (s):
    sys.stderr.write (s + '\n')
    sys.stderr.flush ()

def eprintf (s):
    sys.stderr.write (s)
    sys.stderr.flush ()

# HMM class

class HMM:
    def __init__ (self,data,K,gamma,eta):
        self.K = K
        self.N = len (data)
        self.V = lexicon (data)
        self.eta = eta
        self.gamma = gamma
        self.data = data
        # internal variables
        self.zz  = {}
        self.nz  = np.zeros (K+1)
        self.nzz = np.zeros ((K+1,K+1))
        self.nzw = np.zeros ((K+1,self.V))
        # initialize
        for n in range(len(data)):
            self.zz[n] = []

    def learn (self,iters):
        for iter in range(iters):
            for n in randperm(self.N):
                if (iter > 0):
                    remove_counts (self.data[n], self.zz[n], self.nzz, self.nzw,
                                   self.nz)
                self.zz[n] = ffbs (self.data[n], self.zz[n], self.nzz, self.nzw,
                                   self.nz, self.gamma, self.eta)
                add_counts (self.data[n], self.zz[n], self.nzz, self.nzw, self.nz)
                
            print ('iter[%d]: PPL = %.02f' % \
                   (iter+1,
                   perplexity (self.data,self.nz,self.nzz,self.nzw,self.gamma,self.eta)))
        # model
        model = convert_model (self.zz,self.nz,self.nzz,self.nzw,self.gamma,self.eta)
        return model

    def infer (self, data, states, iter):
        if (iter > 0):
            remove_counts (data, states, self.nzz, self.nzw, self.nz)
        states = ffbs (data, states, self.nzz, self.nzw, self.nz,
                       self.gamma, self.eta)
        add_counts (data, states, self.nzz, self.nzw, self.nz)
        return states

    def dump (self):
        print ('zz =\n', self.zz)
        print ('nz =\n', self.nz)
        print ('nzz =\n', self.nzz)

if __name__ == "__main__":
    main ()
