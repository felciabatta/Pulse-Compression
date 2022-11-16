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

mpl.rcParams['font.serif'] = ['NewComputerModern10']+mpl.rcParamsDefault['font.serif']

mpl.rcParams['font.sans-serif'] = ['NewComputerModernSans10'] + \
    mpl.rcParamsDefault['font.sans-serif']

mpl.rcParams['font.monospace'] = ['NewComputerModernMono10'] + \
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

    def __init__(self, plotfunc, plotargs, plotkwargs={}, title='Title',
                 xlabel=r'$X$', ylabel=r'$Y$',
                 xlim=None, ylim=None, showgrid=False, figsize=(5, 3), dpi=600,
                 xticks=None, yticks=None, axfacecol='w',
                 titlept=14, labelpt=12, tlabelpt=8, subplots=None):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xlim = xlim
        self.ylim = ylim
        self.showgrid = showgrid
        self.axfacecol = axfacecol

        self.titlept = titlept
        self.labelpt = labelpt
        self.tlabelpt = tlabelpt

        self.xticks = xticks
        self.yticks = yticks

        self.dpi = dpi

        self.fig = plt.figure(dpi=self.dpi, figsize=figsize)

        if subplots is None:
            self.ax = self.fig.add_subplot(111)

            plotfunc(*plotargs, **plotkwargs)
            self.set_labels()
            self.set_axes_params()
        else:
            self.ax = []
            for i, sp in enumerate(subplots):
                self.ax.append(self.fig.add_subplot(sp))

                plotfunc(*plotargs[i], **plotkwargs[i])
                self.set_labels(self.ax[i], title[i], xlabel[i], ylabel[i])
                self.set_axes_params(self.ax[i])
        plt.tight_layout()
        plt.show()
        # self.fix_symbols()

    def set_labels(self, ax=None, title=None, xlabel=None, ylabel=None):
        # plt.legend(loc='upper right', markerscale=10, fontsize=tlabelpt,
        # framealpha=0.95, handletextpad=0.2, handlelength=1.)
        if ax is None:
            ax = self.ax
        if title is None:
            title = self.title
        if xlabel is None:
            xlabel = self.xlabel
        if ylabel is None:
            ylabel = self.ylabel

        ax.set_title(title, y=1.0, fontsize=self.titlept)
        ax.set_xlabel(xlabel, fontsize=self.labelpt)
        ax.set_ylabel(ylabel, fontsize=self.labelpt)

    def set_axes_params(self, ax=None, equal_aspect=False, width=0.4):
        if ax is None:
            ax = self.ax

        # limits & aspect
        if equal_aspect:
            ax.set_aspect('equal', 'box')

        ax.set(xlim=self.xlim, ylim=self.ylim)

        # spines & grid
        for s in ax.spines:
            ax.spines[s].set_linewidth(width)

        if self.showgrid:
            ax.grid(color='#e2e2e2', linewidth=width)

        ax.set_facecolor(self.axfacecol)

        # ticks
        ax.tick_params(labelsize=self.tlabelpt, direction='in', width=0.4)

        if self.xticks is not None:
            ax.set_xticks(self.xticks[0], self.xticks[1])
        else:
            ax.ticklabel_format(style='sci', axis='x', scilimits=(-3, 3),
                                     useMathText=True, )
        if self.yticks is not None:
            ax.set_yticks(self.yticks[0], self.yticks[1])
        else:
            ax.ticklabel_format(style='sci', axis='y', scilimits=(-3, 3),
                                 useMathText=True, )

    # def fix_symbols(self):
    #     # print(ax.get_xticklabels()) # for bugfixing
    #     ax.set_xticklabels([i.get_text().replace('−', '$-$')
    #                             for i in ax.get_xticklabels()])
    #     ax.set_yticklabels([i.get_text().replace('−', '$-$')
    #                             for i in ax.get_yticklabels()])

    def save(self, filename=None):
        if filename is None:
            filename = self.title

        if type(filename) == list or type(filename) == tuple:
            ffilename = filename[0]

        filename = self.format_filename(filename)  # remove format characters

        self.fig.savefig('Figures/'+filename+'.pdf', format='pdf',
                         bbox_inches='tight', pad_inches=0, dpi=self.dpi)

    def format_filename(self, mystr=None, chars=['\\,', '$', '\\', '\n', '{', '}']):
        if mystr is None:
            mystr = self.title
        for c in chars:
            mystr = mystr.replace(c, '')
        mystr = mystr.replace('times10^', 'e')

        return mystr
