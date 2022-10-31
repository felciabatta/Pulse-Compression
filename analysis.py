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


# %% EXTRACT REFERENCE PEAK POSITIONS

pulse = signal("signal_data/pulse_2MHznonoise/pulse2mhz.dat",
               "signal_data/pulse_2MHznonoise/bscan.dat")
PLOT = pulse.plot1d(pulse.data_b[300:1000, 70], t=np.arange(300, 1000))
MAP = pulse.plot2d(MIN=0, MAX=0.03)

coordGuessREF = np.array([[426, 10], [536, 25], [647, 40], [757, 55], [868, 70]])

maxCoordsREF, relMaxCoordsREF, _, peakAmplitudes = pulse.find_defects(
    coordGuessREF, pulse.data_b)

MAP.ax.scatter(maxCoordsREF[:, 1], maxCoordsREF[:, 0],
               s=10, c=mycols['sweetpink'], marker='x', zorder=10)

# %% EXTRACT AND PLOT SNR HEATMAP

SNR_Results = np.genfromtxt("Results/SNRResultsEstimate.csv", delimiter=",")

meanTrueSNR_Results = np.genfromtxt("Results/Mean-TrueSNR.csv", delimiter=",")

i_mean = range(5, 24, 6)
i_defects = [i for i in range(24) if i not in i_mean]

means = SNR_Results[:, i_mean]
defects = SNR_Results[:, i_defects]

plt.pcolormesh(np.flip(means, 0))
plt.pcolormesh(np.flip(meanTrueSNR_Results, 0))

# kruskal test
_, pvalue = stats.kruskal(*list(meanTrueSNR_Results)) # signals
_, pvalue = stats.kruskal(*list(meanTrueSNR_Results.transpose())) # filters
