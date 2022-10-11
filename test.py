#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 16:21:47 2022

@author: felixdubicki-piper
"""

import scipy.signal as sg
from numpy import pi
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from signal_data import athena

import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()


# %% Import Data

bscan_filepath = filedialog.askopenfilename()
t, x, data = athena.ReadBScan(bscan_filepath)
data = data

pulse_filepath = filedialog.askopenfilename()
t_p, data_p = athena.ReadAScan(pulse_filepath)

# %% Visualise Ascan

i0 = None
iend = None
# iend = len(data_p)
plt.plot(t[i0:iend], data[i0:iend, 25])

# %% Visualise Ultrasound Pulse Bscan

plt.pcolormesh(data, vmin=.001, vmax=.01)

# %% Visualise Barker Bscan

plt.pcolormesh(data, vmin=0, vmax=.2)

# %% Visualise Bscan Default

plt.pcolormesh(data, vmin=-.1, vmax=.1)

# %% Visualise Pulse
i0 = None
iend = 2000 #500
plt.plot(t_p[:iend], data_p[:iend])

# %% Pulse-Compression

out_signal = np.zeros(data.shape)
for i in range(data.shape[1]):
    out_signal[:, i] = sg.correlate(
        data[:, i], data_p, mode='same')/(0.1*len(data_p))

# plt.pcolormesh(out_signal[877:, :], vmin=0, vmax=50)
plt.pcolormesh(out_signal, vmin=.001, vmax=.01)
plt.pcolormesh(out_signal, vmin=None, vmax=None)
plt.pcolormesh(out_signal, vmin=-.1, vmax=.1)

plt.plot(t, out_signal[:, 25])
