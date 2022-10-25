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

filter_method = {"match": 1, "wien": 2, 'match-wien': 12, 'wien-match': 21}


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

    def match1d(self, remove_pulse=False, s1=None, s2=None, delay=2, trim=0):
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

    def match2d(self, s1=None, s2=None, remove_pulse=False,
                delay=2, trim=0, remove_matchedpulse=0):
        # identical to match1d()
        if s1 is None:
            s1 = np.copy(self.data_b)
        if s2 is None:
            s2 = np.copy(self.data_a)

        if remove_pulse:
            self.remove_excitation(s1, s2, delay=delay, trim=trim)

        self.results = sg.correlate(s1, s2.reshape((-1, 1)),
                                    mode='same')/(0.1*len(self.data_a))

        if remove_matchedpulse:
            self.remove_datapoints(ub=remove_matchedpulse)

    def wien(self, s1=None, s2=None, remove_pulse=False,
             delay=2, trim=0, window=None, power=None):
        if s1 is None:
            s1 = np.copy(self.data_b)
        if s2 is None:
            s2 = np.copy(self.data_a)

        if remove_pulse:
            self.remove_excitation(s1, s2, delay=delay, trim=trim)

        self.results = sg.wiener(s1, window, power)

    def remove_excitation(self, s1, s2, delay=2, trim=0):
        if delay == None:
            delay = np.argmax(s1[:, 1]) - np.argmax(s2)
        s1[delay:delay+len(s2)+trim, :] = 0

    def remove_datapoints(self, signal=None, lb=None, ub=None, newval=0):
        if signal is None:
            signal = self.results
        signal[lb:ub, :] = newval

    def get_max(self, s1=None, s2=None, remove_pulse=1, delay=2, trim=0):
        if s1 is None:
            s1 = np.copy(self.data_b)
        else:
            s1 = np.copy(s1)

        if s2 is None:
            s2 = np.copy(self.data_a)
        else:
            s1 = np.copy(s2)

        if remove_pulse:
            self.remove_excitation(s1, s2, delay=delay, trim=trim)

        return np.max(s1)

    def filter_example(self, filter_method=1, signal=None,
                       remove_pulse=1, trim=0, remove_matchedpulse=0,
                       window=(100, 10),
                       title='Title', x=10, MIN=0, MAX=None,
                       plotresults=(1, 1, 1, 1, 1)):

        if signal is None:
            signal = self.data_b

        if filter_method == 0:
            None

        elif filter_method == 1:
            self.match2d(signal, remove_pulse=remove_pulse, trim=trim,
                         remove_matchedpulse=remove_matchedpulse)

        elif filter_method == 2:
            self.wien(signal, remove_pulse=remove_pulse, trim=trim, window=(100, 10))

        elif filter_method == 12:
            self.match2d(signal, remove_pulse=remove_pulse, trim=trim,
                         remove_matchedpulse=remove_matchedpulse)
            self.wien(self.results, window=(100, 10))

        elif filter_method == 21:
            self.wien(signal, remove_pulse=remove_pulse, trim=trim,
                      window=(100, 10))
            self.match2d(self.results,
                         remove_matchedpulse=remove_matchedpulse)

        if MAX is None:
            MAXbf = 0.7*self.get_max()
            MAXaf = 0.7*self.get_max(self.results)
        else:
            MAXbf = MAX
            MAXaf = MAX

        plotfunc = [self.plot1d, self.plot1d, self.plot1d,
                    self.plot2d, self.plot2d]

        plotargs = [{'title': title},
                    {'data': self.data_b[:, x], 't':self.t_b, 'title':title},
                    {'data': self.results[:, x], 't':self.t_b, 'title':title},
                    {'MIN': MIN, 'MAX': MAXbf, 'title': title},
                    {'data': self.results, 'MIN': MIN, 'MAX': MAXaf, 'title': title}]

        plots = [None]*5

        for i, _ in enumerate(plotresults):
            if plotresults[i]:
                plots[i] = plotfunc[i](**plotargs[i])

        return plots

    def plot1d(self, data=None, t=None, i0=None, iend=None, title=r'Signal',
               xlabel=r'Time, $t\,$seconds', ylabel=r'Amplitude, $A$'):
        if data is None:
            data = self.data_a[i0:iend]
            t = self.t_a[i0:iend]

        plot = LaPlot(plt.plot, [t, data],
                      {'color': mycols['sweetpink'], 'linewidth': 1},
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
                      figsize=(4, 6))
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
        self.results = np.genfromtxt(filepath, delimiter=",")
