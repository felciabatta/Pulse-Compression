#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 17:39:10 2022

@author: felixdubicki-piper
"""

import scipy.signal as sg
from numpy import pi
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from signal_data import athena

from LaTeXplots import LaPlot
from LaTeXplots import mycols

import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()


class signal:
    """


    Parameters
    ----------
    ascan : A-Scan .dat file, optional
        1D data, usually the exitation *(input)* signal.
        The default is None.
    bscan : B-Scan .dat file, optional
        2D data, received echo *(output)* signal. The default is None.
    dataprompt : bool, optional
        Asks for data. The default is True.

    Examples
    -------
    Instantiate a signal object, and perform basic functions:

    >>> # select A-Scan & B-Scan files, respectively, when prompted
    >>> pulse = signal()

    >>> # plot the A-Scan
    >>> pulse.plot1d()

    >>> # plot the B-Scan
    >>> pulse.plot2d()

    >>> # plot the results
    >>> pulse.plot2d(pulse.results)

    >>> # save .csv results; enter filename when prompted
    >>> pulse.save_results()

    To import existing .csv results:

    >>> # select csv file when prompted
    >>> pulse.load_results()

    Notes
    -----
    Upon creating a signal object, and importing A/B-Scan data,
    match filter results are immediately computed automatically.

    *plot2d* has options to modify *MIN* and *MAX* values on colormap

    """

    def __init__(self, ascan=None, bscan=None, dataprompt=True):
        """


        Parameters
        ----------
        ascan : A-Scan .dat file, optional
            1D data, usually the exitation *(input)* signal.
            The default is None.
        bscan : B-Scan .dat file, optional
            2D data, received echo *(output)* signal. The default is None.
        dataprompt : bool, optional
            Asks for data. The default is True.

        Notes
        -----
        Upon creating a signal object, and importing A/B-Scan data,
        match filter results are immediately computed automatically.

        """
        if (ascan is None) and (bscan is None) and not dataprompt:
            None
        else:
            self.load_data(ascan, bscan)

    def load_data(self, ascan=None, bscan=None):
        if ascan is None:
            file_a = filedialog.askopenfilename(initialdir='signal_data/')
        else:
            file_a = ascan

        if bscan is None:
            file_b = filedialog.askopenfilename()
        else:
            file_b = bscan

        self.t_a, self.data_a = athena.ReadAScan(file_a)
        self.t_b, self.x, self.data_b = athena.ReadBScan(file_b)

        self.match2d()

    def match(self, remove_pulse=False, s1=None, s2=None, delay=2, trim=0):
        if s1 is None:
            s1 = np.copy(self.data_b)
        if s2 is None:
            s2 = np.copy(self.data_a)

        if remove_pulse:
            self.remove_excitation(s1, s2, delay=delay, trim=trim)

        out = np.zeros(s1.shape)
        for i in range(s1.shape[1]):
            out[:, i] = sg.correlate(s1[:, i], s2,
                                     mode='same')/(0.1*len(s2))
        self.results = out

    def match2d(self, remove_pulse=False, s1=None, s2=None, delay=2, trim=0):
        # identical to match()
        if s1 is None:
            s1 = np.copy(self.data_b)
        if s2 is None:
            s2 = np.copy(self.data_a)

        if remove_pulse:
            self.remove_excitation(s1, s2, delay=delay, trim=trim)

        out = sg.correlate(s1, s2.reshape((-1, 1)),
                           mode='same')/(0.1*len(self.data_a))
        self.results = out

    def wien(self, signal=None, window=None, power=None):
        if signal is None:
            signal = self.results
        self.results = sg.wiener(signal, window, power)

    def remove_excitation(self, s1, s2, delay=2, trim=0):
        if delay == None:
            delay = np.argmax(s1[:, 1]) - np.argmax(s2)
        s1[delay:delay+len(s2)+trim, :] = 0
        pass

    def plot1d(self, data=None, t=None, i0=None, iend=None, title=r'Signal',
               xlabel=r'Time, $t\,$seconds', ylabel=r'Amplitude, $A$'):
        if data is None:
            data = self.data_a[i0:iend]
            t = self.t_a[i0:iend]

        plot = LaPlot(plt.plot, [t, data],
                      {'color':mycols['sweetpink'], 'linewidth':1},
                      xlim=(t[0], t[-1]), title=title,
                      xlabel=xlabel, ylabel=ylabel, showgrid=1)
        return plot

    def plot2d(self, data=None, t=None, x=None,  MIN=None, MAX=None,
               title=r'Signal', xlabel=r'Position, $x$',
               ylabel=r'Time, $t\,$seconds'):
        if data is None:
            data = self.data_b
            t = self.t_b
            x = self.x
        plot = LaPlot(plt.pcolormesh, [data], {"vmin": MIN, "vmax": MAX},
                      title=title, xlabel=xlabel, ylabel=ylabel, showgrid=0,
                      figsize=(4,6))
        return plot

    def save_results(self, data=None, filename=None):
        if data is None:
            data = self.results
        filepath = filedialog.asksaveasfilename(initialdir='signal_data/',
                                                defaultextension='.csv')
        np.savetxt(filepath, data, delimiter=",")

    def load_results(self, filepath=None):
        if filepath is None:
            filepath = filedialog.askopenfilename()
        results = np.genfromtxt(filepath)
