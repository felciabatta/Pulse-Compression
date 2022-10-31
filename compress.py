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

        self.t_a, self.data_a, self.T_a = athena.ReadAScan(file_a)
        self.t_b, self.x, self.data_b, self.T_b = athena.ReadBScan(file_b)

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

    def prod_filter(self, s1, s2, remove_pulse=False,
                    delay=2, trim=0, window=1, signal_cutoff=1700):
        if s1 is None:
            s1 = np.copy(self.data_b)
        if s2 is None:
            s2 = np.copy(self.data_a)

        if remove_pulse:
            self.remove_excitation(s1, s2, delay=delay, trim=trim)

        window = 1
        T = s1.shape[0]
        N = s1.shape[1] - 2*window
        R = 2*window
        prodarray = np.zeros((T, N))
        for n in range(N):
            x0 = n
            xend = n+2*window+1
            prodarray[:, n] = np.prod(s1[:, x0:xend], 1)
            prodarray[:, n] /= max(prodarray[:signal_cutoff, n])
            # prodarray[:, n] =
            # np.log(abs(prodarray[:, n]))*np.sign(prodarray[:, n])

        self.results = prodarray

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

    def find_defects(self, coordGuess=None, data=None,
                     window=np.array([50, 5])):
        if data is None:
            data = self.results

        if coordGuess is None:
            # coords of defect in US pulse no noise
            coordGuess = np.array(
                [[426, 10], [536, 25], [647, 40], [757, 55], [868, 70]])
        elif coordGuess.size == 2:
            coordGuess = coordGuess + np.array(
                [[0, 0], [110, 15], [221, 30], [331, 45], [442, 60]])

        self.coordError = np.zeros(coordGuess.shape)
        self.peakAmplitudes = np.zeros(coordGuess.shape[0])
        for i, c in enumerate(coordGuess):
            tx0 = c-window
            txend = c+window+1

            maxIndex = np.argmax(data[tx0[0]:txend[0], tx0[1]:txend[1]])
            self.coordError[i] = (np.unravel_index(
                maxIndex, window*2+1) - window).astype(int)

            self.peakAmplitudes[i] = np.amax(
                data[tx0[0]:txend[0], tx0[1]:txend[1]])

        self.maxCoords = (self.coordError + coordGuess).astype(int)
        self.relMaxCoords = (self.maxCoords - self.maxCoords[0]).astype(int)
        return self.maxCoords, self.relMaxCoords, self.coordError, self.peakAmplitudes

    def trueSNR(self, peakAmplitudes=[], s1=None, s2=None,
                removed_pulse=0, delay=2, trim=0, signal_cutoff=1700):
        # TODO: remove peakAmplitude argument
        if s1 is None:
            s1 = self.results
        if s2 is None:
            s2 = self.data_a

        if removed_pulse:
            tend = delay+len(s2)+trim

        totalRMS = np.sqrt(np.mean(s1[tend:signal_cutoff, :]**2))
        self.SNRs = self.peakAmplitudes/totalRMS
        self.SNR = np.mean(self.SNRs)

        return self.SNRs, self.SNR

    def peakWidths(self, peakCoords=None, signal=None, timeformat=1):
        if signal == None:
            signal = self.results
        if peakCoords == None:
            peakCoords = self.maxCoords

        self.defectWidths = np.zeros(len(peakCoords))
        for i, tx in enumerate(peakCoords):
            self.defectWidths[i] = sg.peak_widths(
                signal[:, tx[1]], [tx[0]])[0]

        #TODO: fix bug where width is not found - hence exclude 0s from mean
        self.defectWidth = np.mean(self.defectWidths[self.defectWidths!=0])

        if timeformat:
            self.defectWidths *= self.T_b
            self.defectWidth *= self.T_b
            # print("\nRange resolution is", self.defectWidth.round(8),
            #       "s, \nfrom", list(self.defectWidths.round(8)))
            print("\nRange resolution is", (self.defectWidth/10e-9).round(1),
                  "ns, \nfrom", list((self.defectWidths/10e-9).round(1)))
        else:
            print("\nRange resolution is ", self.defectWidth.round(2),
                  "samples, \nfrom", list(self.defectWidths.around(2)))

        return self.defectWidths, self.defectWidth

    def peakSidelobeRatio(self, peakCoords=None, signal=None):
        """Find Peak Side Lobe Ratio"""
        if signal == None:
            signal = self.results
        if peakCoords == None:
            peakCoords = self.maxCoords

        self.PSRs = np.zeros(len(peakCoords))
        for i, tx in enumerate(peakCoords):
            peaks, properties = sg.find_peaks(signal[:, tx[1]], height=0)

            # note that the defect in peakCoords may not appear in peaks
            # as the original defect finder took max in a reigon, so if the max
            # lay on a boundary, it is not guarateed to be a peak
            # INSTEAD, we just take closest peak, to the "located defect"
            peak_i = np.abs(peaks - tx[0]).argmin()

            # redundant - unless change peak finding code to use find peaks, rather than max
            # peak_i = np.where(peaks == tx[0])[0][0]

            sides_t = peaks[[peak_i-1, peak_i+1]]
            meanPS = np.mean(signal[sides_t, tx[1]])
            self.PSRs[i] = signal[tx[0], tx[1]]/meanPS

        self.PSR = np.mean(self.PSRs)

        print("\nPeak Sidelobe Ratio is", self.PSR.round(1),
              ", \nfrom", list(self.PSRs.round(1)))

        return self.PSRs, self.PSR

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
            self.wien(signal, remove_pulse=remove_pulse,
                      trim=trim, window=(100, 10))

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

    def SNR_example(self, coordGuess, plots, signal=None, plotMyGuess=0,
                    window=np.array([50, 5]), removed_pulse=1, delay=2,
                    trim=0):
        if signal is None:
            signal = self.results

        if coordGuess is None:
            # coords of defect in US pulse no noise
            coordGuess = np.array(
                [[426, 10], [536, 25], [647, 40], [757, 55], [868, 70]])
        elif np.array(coordGuess).size == 2:
            coordGuess = coordGuess + np.array(
                [[0, 0], [110, 15], [221, 30], [331, 45], [442, 60]])

        if plotMyGuess:
            plots[-1].ax.scatter(coordGuess[:, 1], coordGuess[:, 0],
                                 s=10, c=mycols['calmblue'], marker='x',
                                 zorder=10)

        maxCoords, _, _, peakAmplitudes = self.find_defects(coordGuess,
                                                            window=window)
        SNRs, SNR = self.trueSNR(peakAmplitudes, removed_pulse=removed_pulse,
                                 delay=delay, trim=trim)
        plots[-1].ax.scatter(maxCoords[:, 1], maxCoords[:, 0], s=10,
                             c=mycols['sweetpink'], marker='x', zorder=10)

        print("\nSNR is "+str(SNR.round(1))+" from", list(SNRs.round(1)))

        return maxCoords, SNRs, SNR

    def plot1d(self, data=None, t=None, i0=None, iend=None, title=r'Signal',
               xlabel=r'Time, $t\,$seconds', ylabel=r'Amplitude, $A$',
               ylim=None):
        if data is None:
            data = self.data_a[i0:iend]
            t = self.t_a[i0:iend]

        plot = LaPlot(plt.plot, [t, data],
                      {'color': mycols['sweetpink'], 'linewidth': 1},
                      xlim=(t[0], t[-1]), ylim=ylim, title=title,
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
