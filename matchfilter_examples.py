#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 23:06:59 2022

@author: felixdubicki-piper
"""

from compress import *

# %% CLEAN U.S. PULSE, 2MHz

pulse = signal("signal_data/pulse_2MHznonoise/pulse2mhz.dat",
               "signal_data/pulse_2MHznonoise/bscan.dat")

pulse.plot1d()
pulse.plot2d(MIN=0, MAX=0.04)
pulse.plot2d(pulse.results, MIN=0, MAX=0.04)
pulse.plot1d(pulse.data_b[:, 10], pulse.t_b)
pulse.plot1d(pulse.results[:, 10], pulse.t_b)

# %% U.S. PULSE, 1MHz

pulse1 = signal("signal_data/pulse_1MHznoise/pulse1mhz.dat",
                "signal_data/pulse_1MHznoise/bscanpulse1.dat")

pulse1.plot1d()
pulse1.plot2d(MIN=0, MAX=0.08)
pulse1.plot2d(pulse1.results, MIN=0, MAX=0.08)
pulse1.plot1d(pulse1.data_b[:, 10], pulse1.t_b)
pulse1.plot1d(pulse1.results[:, 10], pulse1.t_b)

# %% U.S. PULSE, 2MHz

pulse2 = signal("signal_data/pulse_2MHznoise/pulse2mhz.dat",
                "signal_data/pulse_2MHznoise/bscanpulse2.dat")

pulse2.plot1d()
pulse2.plot2d(MIN=0, MAX=0.02)
pulse2.plot2d(pulse2.results, MIN=0, MAX=0.02)
pulse2.plot1d(pulse2.data_b[:, 10], pulse2.t_b)
pulse2.plot1d(pulse2.results[:, 10], pulse2.t_b)

# %% Short Chirp, 0.8-2.2MHz

chirpS = signal("signal_data/chirp_0822MHz_2u/chirpsignal.dat",
                "signal_data/chirp_0822MHz_2u/bscanchirp0822.dat")

chirpS.plot1d()
chirpS.plot2d(MIN=0, MAX=0.08)
chirpS.plot2d(chirpS.results, MIN=0, MAX=0.2)
chirpS.plot1d(chirpS.data_b[:, 10], chirpS.t_b)
chirpS.plot1d(chirpS.results[:, 10], chirpS.t_b)

# %% Long Chirp, 0.8-2.2MHz

chirpL = signal("signal_data/chirp_0822MHz_6u/longchirp.dat",
                "signal_data/chirp_0822MHz_6u/bscan.dat")

chirpL.plot1d()
chirpL.plot2d(MIN=0, MAX=0.08)
chirpL.plot2d(chirpL.results, MIN=0, MAX=0.2)
chirpL.plot1d(chirpL.data_b[:, 10], chirpL.t_b)
chirpL.plot1d(chirpL.results[:, 10], chirpL.t_b)

# Pulse Cancellation

CC = sg.correlate(chirpL.data_a, chirpL.data_a)
N = len(CC)
M = len(chirpL.results[:, 10])
n = np.argmax(CC)
m = np.argmax(chirpL.results[:, 10])
p = np.max(CC)
q = np.max(chirpL.results[:, 10])
pad1 = np.concatenate((np.zeros(N),
                      chirpL.results[:, 10],
                      np.zeros(N)))
pad2 = np.concatenate((np.zeros(N+m-n),
                       CC*(q/p),
                       np.zeros(M-m+n)))

newresult = (pad1 - pad2)[N:N+M]

# %% Barker 13, 1MHz

bark1 = signal("signal_data/barker_1MHz_13/signalbarker13.dat",
               "signal_data/barker_1MHz_13/bscanbarker13.dat")

bark1.plot1d()
bark1.plot2d(MIN=0, MAX=0.2)
bark1.plot2d(bark1.results, MIN=0, MAX=0.4)
bark1.plot1d(bark1.data_b[:, 10], bark1.t_b)
bark1.plot1d(bark1.results[:, 10], bark1.t_b)

# %% ... with Pulse Cancellation
# iterate this, to eliminate more peaks

CC = sg.correlate(bark1.data_a, bark1.data_a)
N = len(CC)
M = len(bark1.results[:, 10])
n = np.argmax(CC)
m = np.argmax(bark1.results[:, 10])
p = np.max(CC)
q = np.max(bark1.results[:, 10])
pad1 = np.concatenate((np.zeros(N),
                      bark1.results[:, 10],
                      np.zeros(N)))
pad2 = np.concatenate((np.zeros(N+m-n),
                       CC*(q/p),
                       np.zeros(M-m+n)))

newresult = (pad1 - pad2)[N:N+M]

# %% Barker 13, 2MHz

bark2 = signal("signal_data/barker_2MHz_13/barker13.dat",
               "signal_data/barker_2MHz_13/bscanbarker13.dat")

bark2.plot1d()
bark2.plot2d(MIN=0, MAX=0.2)
bark2.plot2d(bark2.results, MIN=0, MAX=0.2)
bark2.plot1d(bark2.data_b[:, 10], bark2.t_b)
bark2.plot1d(bark2.results[:, 10], bark2.t_b)

# %% ... with Pulse Cancellation
# iterate this, to eliminate more peaks

CC = sg.correlate(bark2.data_a, bark2.data_a)
N = len(CC)
M = len(bark2.results[:, 10])
n = np.argmax(CC)
m = np.argmax(bark2.results[:, 10])
p = np.max(CC)
q = np.max(bark2.results[:, 10])
pad1 = np.concatenate((np.zeros(N),
                      bark2.results[:, 10],
                      np.zeros(N)))
pad2 = np.concatenate((np.zeros(N+m-n),
                       CC*(q/p),
                       np.zeros(M-m+n)))

newresult = (pad1 - pad2)[N:N+M]

# %% Golay 3, 2MHz

# main signal
golay = signal("signal_data/golay/golay_a_l3_2.dat",
               "signal_data/golay/bscangolay2mhz_l3nc.dat")

golay.plot1d()
golay.plot2d(MIN=0, MAX=0.1)
golay.plot2d(golay.results, MIN=0, MAX=0.2)
golay.plot1d(golay.data_b[:, 10], golay.t_b)
golay.plot1d(golay.results[:, 10], golay.t_b)

# complementary signal
golayC = signal("signal_data/golay/golay_l3_2c.dat",
               "signal_data/golay/bscangolay2mhz_l3c.dat")

golayC.plot1d()
golayC.plot2d(MIN=0, MAX=0.1)
golayC.plot2d(golayC.results, MIN=0, MAX=0.2)
golayC.plot1d(golayC.data_b[:, 10], golayC.t_b)
golayC.plot1d(golayC.results[:, 10], golayC.t_b)

# sum of correlated main & complementary signals
golay_sum = signal("signal_data/golay/golay_a_l3_2.dat",
                   "signal_data/golay/bscangolay2mhz_l3nc.dat")
golay_sum.results = golay.results + golayC.results

golay_sum.plot2d(golay_sum.results, MIN=0, MAX=0.2)
golay_sum.plot1d(golay_sum.results[:, 10], golay_sum.t_b)
