#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:23:26 2022

@author: felixdubicki-piper
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from compress import signal
from LaTeXplots import mycols
from LaTeXplots import LaPlot


# %% EXTRACT REFERENCE PEAK POSITIONS

pulse = signal("signal_data/pulse_2MHznonoise/pulse2mhz.dat",
               "signal_data/pulse_2MHznonoise/bscan.dat")
PLOT = pulse.plot1d(pulse.data_b[300:1000, 70], t=np.arange(300, 1000))
MAP = pulse.plot2d(MIN=0, MAX=0.03)

coordGuessREF = np.array(
    [[426, 10], [536, 25], [647, 40], [757, 55], [868, 70]])

maxCoordsREF, relMaxCoordsREF, _, peakAmplitudes = pulse.find_defects(
    coordGuessREF, pulse.data_b)

MAP.ax.scatter(maxCoordsREF[:, 1], maxCoordsREF[:, 0],
               s=10, c=mycols['sweetpink'], marker='x', zorder=10)

# %% EXTRACT DATA

SNR_Results = np.genfromtxt("Results/SNRResultsEstimate.csv", delimiter=",")

meanTrueSNR_Results = np.genfromtxt("Results/Mean-TrueSNR.csv", delimiter=",")
meanPSR_Results = np.genfromtxt("Results/Mean-PSR.csv", delimiter=",")
meanRangeRsn_Results = np.genfromtxt(
    "Results/Mean-RangeRSN.csv", delimiter=",")
w_SNR, w_PSR = 0.5, 0.5
weighted_SNR_PSR = w_SNR*meanTrueSNR_Results+w_PSR*meanPSR_Results

i_mean = range(5, 24, 6)
i_defects = [i for i in range(24) if i not in i_mean]

means = SNR_Results[:, i_mean]
defects = SNR_Results[:, i_defects]

# %% ORDER DATA ROWS & COLS by MEAN


def order(data, orderfunc):
    row_eval = orderfunc(data, 1)
    col_eval = orderfunc(data, 0)

    row_order = np.argsort(row_eval)
    col_order = np.argsort(col_eval)

    data = data[row_order, :]
    data = data[:, col_order]

    return data, row_order, col_order


# %% RESULTS PLOT FUNC

def results_plot(data, orderfunc=np.mean, title='Title', MIN=None, MAX=None):
    data, ro, co = order(data, orderfunc)

    xlbl, ylbl = r"Filter Method", r"Input Signal"
    xlbl, ylbl = None, None

    flbl = np.array(["Match", "Wien",
                     'Match'+u'\u2013'+'Wien',
                     'Wien'+u'\u2013'+'Match'])
    slbl = np.array([r'Barker $13$'+'\n'+r'$1\,$MHz',
                     r'Barker $13$'+'\n'+r'$2\,$MHz',
                     r'Chirp $2\,\mu$s'+'\n'+r'$0.8\,$-$\,2.2\,$MHz',
                     r'Chirp $6\,\mu$s'+'\n'+r'$0.8\,$-$\,2.2\,$MHz',
                     r'Golay $3$'+'\n'+r'$2\,$MHz',
                     r'U.S. Pulse'+'\n'+r'$1\,$MHz',
                     r'U.S. Pulse'+'\n'+r'$2\,$MHz'])

    xtk = (np.arange(0.5, 4, 1), flbl[co])
    ytk = (np.arange(0.5, 7, 1), slbl[ro])

    kwargs = {'cmap': 'bone', "rasterized": 0, "snap": 1, "edgecolors": "face",
              'vmin': MIN, 'vmax': MAX}

    plot = LaPlot(plt.pcolormesh, (data,), kwargs,
                  title=title,
                  xlabel=xlbl, ylabel=ylbl,
                  xticks=xtk, yticks=ytk, figsize=np.array((4, 5.5))*.85)

    return plot


# %% PLOT SNR HEATMAP

# xlbl, ylbl = r"Filter Method", r"Input Signal"
# xlbl, ylbl = None, None

# flbl = ["Match", "Wien", "Match-Wien", "Wien-Match"]
# slbl = [r'Barker $13$'+'\n'+r'$1\,$MHz',
#         r'Barker $13$'+'\n'+r'$2\,$MHz',
#         r'Chirp $2\,\mu$s'+'\n'+r'$0.8\,$-$\,2.2\,$MHz',
#         r'Chirp $6\,\mu$s'+'\n'+r'$0.8\,$-$\,2.2\,$MHz',
#         r'Golay $3$'+'\n'+r'$2\,$MHz',
#         r'U.S. Pulse'+'\n'+r'$1\,$MHz',
#         r'U.S. Pulse'+'\n'+r'$2\,$MHz']

# xtk = np.arange(0.5, 4, 1)
# ytk = np.arange(0.5, 7, 1)
# cmap = 'bone'
# kwargs = {'cmap':cmap, "rasterized": 0, "snap": 1, "edgecolors": "face"}
# figsize = (4, 5.5)

orderfunc = np.mean
save_results = 0

MAX = np.max((meanTrueSNR_Results, meanPSR_Results))
MIN = np.min((meanTrueSNR_Results, meanPSR_Results))

PLOT1 = results_plot(means, orderfunc,
                     'Estimate Signal'+u'\u2013'+'Noise Ratio')

PLOT2 = results_plot(meanTrueSNR_Results, orderfunc,
                     'True Signal'+u'\u2013'+'Noise Ratio', MIN, MAX)

PLOT3 = results_plot(meanPSR_Results, orderfunc,
                     'Peak'+u'\u2013'+'Sidelobe Ratio', MIN, MAX)

PLOT4 = results_plot(weighted_SNR_PSR, orderfunc,
                     rf'${w_SNR}\,$SNR + ${w_PSR}\,$PSR', MIN, MAX)

PLOT5 = results_plot(-meanRangeRsn_Results, orderfunc,
                     'Spatial Resolution')


# PLOT2 = LaPlot(plt.pcolormesh,
#                (order(, np.mean)[0],),
#                kwargs,
#                title='True Signal'+u'\u2013'+'Noise Ratio',
#                xlabel=xlbl, ylabel=ylbl,
#                xticks=xtk, yticks=ytk, figsize=figsize)

# PLOT3 = LaPlot(plt.pcolormesh,
#                (order(, np.mean)[0],),
#                kwargs,
#                title=,
#                xlabel=xlbl, ylabel=ylbl,
#                xticks=xtk, yticks=ytk, figsize=figsize)

# PLOT4 = LaPlot(plt.pcolormesh,
#                (order(, np.mean)[0],),
#                kwargs,
#                title=,
#                xlabel=xlbl, ylabel=ylbl,
#                xticks=xtk, yticks=ytk, figsize=figsize)

# PLOT5 = LaPlot(plt.pcolormesh,
#                (order(, np.mean)[0],),
#                kwargs,
#                title=,
#                xlabel=xlbl, ylabel=ylbl,
#                xticks=xtk, yticks=ytk, figsize=figsize)

PLOTs = [PLOT1, PLOT2, PLOT3, PLOT4, PLOT5]
for p in PLOTs:
    if save_results:
        p.save()

# kruskal test
_, pvalue = stats.kruskal(*list(meanTrueSNR_Results))  # signals
_, pvalue = stats.kruskal(*list(meanTrueSNR_Results.transpose()))  # filters


signalMeanSNRs = np.mean(meanTrueSNR_Results, 1)
filterMeanSNRs = np.mean(meanTrueSNR_Results, 0)

signalMeanPSRs = np.mean(meanPSR_Results, 1)
filterMeanPSRs = np.mean(meanPSR_Results, 0)
