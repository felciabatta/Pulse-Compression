#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 23:25:27 2022

@author: felixdubicki-piper
"""

"""
Script to format plots in suitable style for LaTeX
"""


# ======= ====================================================================
#  FONTS
# ======= ====================================================================

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
mpl.rcdefaults()

mpl.rcParams['font.family'] = ['serif']

mpl.rcParams['font.serif'] = ['CMU Serif']+mpl.rcParamsDefault['font.serif']

mpl.rcParams['font.sans-serif'] = ['CMU Sans Serif'] + \
    mpl.rcParamsDefault['font.sans-serif']

mpl.rcParams['mathtext.fontset'] = 'cm'

mpl.rcParams['axes.unicode_minus'] = True  # TODO: sort this issuse

# mpl.rcParams["axes.formatter.use_mathtext"] = True

# ======== ===================================================================
#  COLORS
# ======== ===================================================================

mycols = {'sweetpink': '#ff4ab9', 'calmblue': '#00a8e3'}


# ====== =====================================================================
#  PLOT
# ====== =====================================================================

class LaPlot:
    """Create figure & axes formatted like LaTeX
    """

    def __init__(self, plotfunc, plotargs, plotkwargs={}, title='Title', xlabel=r'$X$ - is a dash, $-0.50$ is a minus', ylabel=r'$Y$',
                 xlim=None, ylim=None, showgrid=False, figsize=(5,3)):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xlim = xlim
        self.ylim = ylim
        self.showgrid = showgrid

        self.fig = plt.figure(dpi=250, figsize=figsize)
        self.ax = self.fig.add_subplot(111)

        plotfunc(*plotargs, **plotkwargs)
        self.set_labels()
        self.set_axes_params()
        plt.show()
        self.fix_symbols()

    def set_labels(self, titlept=16, labelpt=12, tlabelpt=10):
        # plt.legend(loc='upper right', markerscale=10, fontsize=tlabelpt,
        # framealpha=0.95, handletextpad=0.2, handlelength=1.)

        self.ax.set_title(self.title, y=1.0, fontsize=titlept)
        self.ax.set_xlabel(self.xlabel, fontsize=labelpt)
        self.ax.set_ylabel(self.ylabel, fontsize=labelpt)

    def set_axes_params(self, equal_aspect=False, width=0.4, tlabelpt=10):
        # limits & aspect
        if equal_aspect:
            self.ax.set_aspect('equal', 'box')

        self.ax.set(xlim=self.xlim, ylim=self.ylim)

        # spines & grid
        for s in self.ax.spines:
            self.ax.spines[s].set_linewidth(width)

        if self.showgrid:
            self.ax.grid(color='#e2e2e2', linewidth=width)

        # ticks
        self.ax.tick_params(labelsize=tlabelpt, direction='in', width=0.4)

    def fix_symbols(self):
        # print(self.ax.get_xticklabels()) # for bugfixing
        self.ax.set_xticklabels([i.get_text().replace('−', '$-$')
                                for i in self.ax.get_xticklabels()])
        self.ax.set_yticklabels([i.get_text().replace('−', '$-$')
                                for i in self.ax.get_yticklabels()])

    def save(self, filename=None):
        if filename is None:
            filename = self.title
        filename = self.format_filename(filename) # remove format characters

        self.fig.savefig('Figures/'+filename+'.pdf', format='pdf',
                         bbox_inches='tight', pad_inches=0)

    def format_filename(self, mystr=None, chars=['\\,', '$', '\\', '\n']):
        if mystr is None:
            mystr = self.title

        for c in chars:
            mystr = mystr.replace(c, '')

        return mystr
