#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:23:26 2022

@author: felixdubicki-piper
"""

import numpy as np
import matplotlib.pyplot as plt
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

# %% EXTRACT BARKER 2MHz PEAKS

bark2 = signal("signal_data/barker_2MHz_13/barker13.dat",
               "signal_data/barker_2MHz_13/bscanbarker13.dat")
title = r'Barker Code (length $13$), $1\,$MHz'

plots = bark2.filter_example(filter_method=12, title=title, x=10)
maxCoords, SNRs, SNR = bark2.SNR_example([575, 10], plots)

# %%

SNR_Results = np.genfromtxt("SNR_Results.csv", delimiter=",")

i_mean = range(5, 24, 6)
i_defects = [i for i in range(24) if i not in i_mean]

means = SNR_Results[:, i_mean]
defects = SNR_Results[:, i_defects]

plt.pcolormesh(np.flip(means, 0))
