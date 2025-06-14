#!/bin/env python
#
#    putil.py
#    Matplot plotting utilities.
#    $Id: putil.py,v 1.19 2024/03/02 02:06:12 daichi Exp $
#
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from pylab import *

# xrange, yrange.
def xrange (spec):
    gca().set_xlim (spec)

def tick_top ():
    gca().xaxis.tick_top ()

# xtick, ytick interval.
def xtickwidth (n, ax=None):
    ax_ = gca() if ax is None else ax
    ax_.xaxis.set_major_locator (MultipleLocator(n))

def ytickwidth (n, ax=None):
    ax_ = gca() if ax is None else ax
    ax_.yaxis.set_major_locator (MultipleLocator(n))

# global fontsize.
def fontsize (n):
    plt.rcParams['font.size'] = n

# global figure size.
def figsize (size): # eg. figsize((10,3))
    return figure (figsize=size)

# tick fontsize.
def ticksize (n):
    tick_params (axis='both', which='major', labelsize=n)

def xticksize (n):
    tick_params (axis='x', which='major', labelsize=n)

def yticksize (n):
    tick_params (axis='y', which='major', labelsize=n)
    
# use LaTeX.
def usetex ():
    plt.rcParams['text.usetex'] = True

# simple 3D plot.
def simple3d (ax):
    ax.grid (False)
    # ax.set_aspect ('equal')
    ax.view_init (30,-110)
    ax.tick_params(axis='x',pad=7)
    ax.xaxis.set_rotate_label (False)
    ax.yaxis.set_rotate_label (False)    
    ax.xaxis.set_pane_color((1,1,1,1))
    ax.yaxis.set_pane_color((1,1,1,1))

# set aspect ratio.
def aspect_ratio (r):
    gca().set_aspect (r)

def figaspect (r):
    figure (figsize=matplotlib.figure.figaspect(r))

# set font specification.
def setfonts(spec):
    matplotlib.rc('font', **spec)

# set default line widths.
def linewidth(n):
    matplotlib.rcParams['axes.linewidth'] = n

# 'nomirror' in Gnuplot.
def nomirror():
    ax = gca()
    ax.yaxis.tick_left()
    ax.xaxis.tick_bottom()

# axes lie on zeros.
def zero_origin():
    ax = axes()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    
def zero_origin_x():
    ax = axes()
    ax.spines['bottom'].set_position('zero')

def zero_origin_y():
    ax = axes()
    ax.spines['left'].set_position('zero')

# leave only left and bottom axis.
# eg: putil.simpleaxis()
def simpleaxis():
    ax = gca().axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

# one dimensional plot.
def one_dimensional():
    axes().spines['left'].set_visible(False)
    tick_params (
        left='off',
        labelleft='off'
    )

# plot with no axes.
def no_axis ():
    ax = gca().axes
    for dir in ['left','right','top','bottom']:
        ax.spines[dir].set_visible (False)
    tick_params (
        left = 'off', right = 'off', top = 'off', bottom = 'off',
        labelleft = 'off', labelbottom = 'off'
    )

# add 'x' and 'y'.
def add_xy (x=0.0,y=0.0):
    ax = gca().axes
    if x == 0.0 or y == 0.0:
        x = ax.get_xlim()[1] + 0.1
        y = ax.get_ylim()[1] + 0.18
    ax.text(x,0,r'$x$',va='center',fontsize=20)
    ax.text(0,y,r'$y$',ha='center',fontsize=20)

def add_x (x=0.0):
    ax = gca().axes
    if x == 0.0:
        x = ax.get_xlim()[1] + 0.1
    # ax.text(x,0,r'$x$',va='center')
    ax.text(x,0,'x',va='center',style='italic')

def add_y (y=0.0):
    ax = gca().axes
    if y == 0.0:
        y = ax.get_ylim()[1] + 0.1
    # ax.text(0,y,r'$y$',ha='center')
    ax.text(0,y,'y',ha='center',style='italic')
    
# set margins outside of labels.
# eg: putil.margins(left=0.1,bottom=0.2)
margins = matplotlib.pyplot.subplots_adjust

#
# Ticks
#

def no_ticks (ax=None):
    if ax is None:
        ax = gca()
    ax.get_xaxis().set_ticks ([])
    ax.get_yaxis().set_ticks ([])

def no_xticks (ax=None):
    if ax is None:
        ax = axes()
    ax.get_xaxis().set_ticks ([])

def no_yticks (ax=None):
    if ax is None:
        ax = axes()
    ax.get_yaxis().set_ticks ([])
    
# padding of xticks and yticks.
def tickpad(n):
    axes().tick_params(direction='out',pad=n)
def xtickpad(n):
    gca().get_xaxis().set_tick_params(direction='out',pad=n)
def ytickpad(n):
    gca().get_yaxis().set_tick_params(direction='out',pad=n)

# xtick and ytick labels.
# usage: xticklabels(("foo","bar"))
def xticklabels(s):
    gca().set_xticklabels(s)
def yticklabels(s):
    gca().set_yticklabels(s)

# set ticks size.
# usage: ticksize2(10,1)
def ticksize2(length,width):
    for line in gca().get_xticklines() + gca().get_yticklines():
        line.set_markersize(length)
        line.set_markeredgewidth(width)

def savefig (file, **args):
    plt.savefig (file, bbox_inches='tight', **args)

# increase plot area for labels.
def add_bottom (p):
    gcf().subplots_adjust (bottom=p)
def add_left (p):
    gcf().subplots_adjust (left=p)

# axis() in 3d.
def axis3 (ax, lims):
    ax.set_xlim (lims[0], lims[1])
    ax.set_ylim (lims[2], lims[3])
    ax.set_zlim (lims[4], lims[5])

# use TeX.
def usetex ():
    mpl.rc('text', usetex=True)
    mpl.rcParams['text.latex.preamble'] = r"\usepackage{bm}\usepackage{helvet}"
    fmt = mpl.ticker.StrMethodFormatter("{x}")
    gca().xaxis.set_major_formatter(fmt)
    gca().yaxis.set_major_formatter(fmt)

