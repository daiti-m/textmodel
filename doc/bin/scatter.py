#!/usr/local/bin/python

import sys
import putil
import numpy as np
from pylab import *
from sklearn.decomposition import PCA, FastICA

def pca (X):
    X = X - np.mean (X, axis=0)
    analyzer = PCA ()
    S,M = analyzer.fit_transform(X), analyzer.components_.T
    return S / np.std(S,axis=0), M
    
def ica (X):
    X = X - np.mean (X, axis=0)
    analyzer = FastICA (whiten='arbitrary-variance')
    S = analyzer.fit_transform (X)
    S /= np.std(S)
    return S, analyzer.mixing_

def draw (ax, xx, yy, title=None):
    ax.scatter (xx, yy, marker='x', color='k', linewidth=0.5)
    ax.set_aspect (1)
    ax.axis ([-2.5,2.5,-2.5,2.5])
    if title is not None:
        ax.set_title (title, pad=13)

def draw_axis (ax, axis, label, style='solid'):
    axis /= axis.std()
    if label == 'ICA':
        axis *= 0.8
    else:
        axis *= 1.2
    x,y = axis
    if style == 'solid':
        ax.quiver (
            (0,0),(0,0),x,y,scale=6,width=0.02,label=label,
            linestyle=style,linewidth=1,fc='black',ec='black'
        )
    else:
        ax.quiver (
            (0,0),(0,0),x,y,scale=6,width=0.02,label=label,
            linestyle='solid',linewidth=1,fc='none',ec='black'
        )

# def draw_axis (ax, axis, color, label):
#     axis /= axis.std()
#     x,y = axis
#     ax.quiver (
#         (0,0),(0,0),x,y,color=color,
#         scale=6,width=0.02,label=label
#     )

def main ():
    N = 60
    xx1 = rand(N) * 4 - 2; xx2 = rand(N) * 4 - 2
    yy1 = xx1 * 0.5 + 0.2 * randn(N)
    yy2 = xx2 * 2 + 0.2 * randn(N)
    xx = np.hstack((xx1,xx2))
    yy = np.hstack((yy1,yy2))

    fig,ax = subplots (1,3,figsize=(8,3))
    X = np.vstack ((xx,yy)).T
    
    S,C = ica (X)
    Spca,Cpca = pca (X)

    draw (ax[0], xx, yy, "data")
    draw_axis (ax[0], C, 'ICA', 'solid')
    draw_axis (ax[0], Cpca, 'PCA', 'dashed')

    draw (ax[1], Spca[:,0], Spca[:,1], "PCA")
    
    draw (ax[2], S[:,0], S[:,1], "ICA")

    fig.subplots_adjust (wspace=0.4)

    if len(sys.argv) > 1:
        putil.savefig (sys.argv[1], dpi=300)
    show ()



if __name__ == "__main__":
    main ()
