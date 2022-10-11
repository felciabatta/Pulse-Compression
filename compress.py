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

        self.match()

    def match(self):
        out = np.zeros(self.data_b.shape)
        for i in range(self.data_b.shape[1]):
            out[:, i] = sg.correlate(self.data_b[:, i],
                                     self.data_a,
                                     mode='same')/(0.1*len(self.data_a))
        self.results = out

    def match2d(self):
        # identical to match()
        out = sg.correlate(self.data_b, self.data_a.reshape((-1,1)),
                           mode='same')/(0.1*len(self.data_a))
        self.results = out

    def plot1d(self, data=None, t=None, i0=None, iend=None):
        if data is None:
            data = self.data_a
            t = self.t_a
        fig = plt.figure()
        plt.plot(t[i0:iend], data[i0:iend])
        return fig

    def plot2d(self, data=None, t=None, x=None,  MIN=None, MAX=None):
        if data is None:
            data = self.data_b
            t = self.t_b
            x = self.x
        fig = plt.figure()
        plt.pcolormesh(data, vmin=MIN, vmax=MAX)
        return fig

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
