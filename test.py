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
t, x, data = Athena.ReadBScan(bscan_filepath)
data = data

pulse_filepath = filedialog.askopenfilename()
t_p, data_p = Athena.ReadAScan(pulse_filepath)

# %% Visualise Ascan

i0 = None
iend = len(data_p) #None #500 #
plt.plot(t[i0:iend], data[i0:iend, 10])

# %% Visualise Ultrasound Pulse Bscan

plt.pcolormesh(data, vmin=.001, vmax=.01)

# %% Visualise Barker Bscan

plt.pcolormesh(data, vmin=0, vmax=.2)

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

# plt.plot(t, out_signal[:, 10])

# %% Pulse-Compression (With Data Correction NOT NEEDED ANYMORE)
# This issue was only for the no-noise data, but this is fixed now

out_signal = np.repeat(np.zeros(data.shape), 2, axis=0)
for i in range(data.shape[1]):
    out_signal[:, i] = sg.correlate(
        np.repeat(data[:, i], 2, axis=0), data_p, mode='same')/(0.1*len(data_p))

# plt.pcolormesh(out_signal[877:, :], vmin=0, vmax=50)
# plt.pcolormesh(out_signal, vmin=.001, vmax=.005)
# plt.pcolormesh(out_signal, vmin=.0, vmax=.001)
# plt.pcolormesh(out_signal)


plt.plot(np.repeat(t, 2, axis=0), out_signal[:, 10])
