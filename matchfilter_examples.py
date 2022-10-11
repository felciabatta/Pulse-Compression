#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 23:06:59 2022

@author: felixdubicki-piper
"""

from compress import signal

# %% CLEAN U.S. PULSE, 2MHz

pulse = signal("signal_data/pulse_2MHznonoise/pulse2mhz.dat",
               "signal_data/pulse_2MHznonoise/bscan.dat")

pulse.plot1d()
pulse.plot2d(MIN=0, MAX=0.04)
pulse.plot2d(pulse.results, MIN=0, MAX=0.04)
pulse.plot1d(pulse.data_b[:,10], pulse.t_b)
pulse.plot1d(pulse.results[:,10], pulse.t_b)

# %% U.S. PULSE, 1MHz

pulse1 = signal("signal_data/pulse_1MHznoise/pulse1mhz.dat",
               "signal_data/pulse_1MHznoise/bscanpulse1.dat")

pulse1.plot1d()
pulse1.plot2d(MIN=0, MAX=0.08)
pulse1.plot2d(pulse1.results, MIN=0, MAX=0.08)
pulse1.plot1d(pulse1.data_b[:,10], pulse1.t_b)
pulse1.plot1d(pulse1.results[:,10], pulse1.t_b)

# %% U.S. PULSE, 2MHz

pulse2 = signal("signal_data/pulse_2MHznoise/pulse2mhz.dat",
               "signal_data/pulse_2MHznoise/bscanpulse2.dat")

pulse2.plot1d()
pulse2.plot2d(MIN=0, MAX=0.02)
pulse2.plot2d(pulse2.results, MIN=0, MAX=0.02)
pulse2.plot1d(pulse2.data_b[:,10], pulse2.t_b)
pulse2.plot1d(pulse2.results[:,10], pulse2.t_b)

# %% Short Chirp, 0.8-2.2MHz

chirpS = signal("signal_data/chirp_0822MHz_2u/chirpsignal.dat",
               "signal_data/chirp_0822MHz_2u/bscanchirp0822.dat")

chirpS.plot1d()
chirpS.plot2d(MIN=0, MAX=0.08)
chirpS.plot2d(chirpS.results, MIN=0, MAX=0.2)
chirpS.plot1d(chirpS.data_b[:,10], chirpS.t_b)
chirpS.plot1d(chirpS.results[:,10], chirpS.t_b)

# %% Long Chirp, 0.8-2.2MHz

chirpL = signal("signal_data/chirp_0822MHz_6u/longchirp.dat",
               "signal_data/chirp_0822MHz_6u/bscan.dat")

chirpL.plot1d()
chirpL.plot2d(MIN=0, MAX=0.08)
chirpL.plot2d(chirpL.results, MIN=0, MAX=0.2)
chirpL.plot1d(chirpL.data_b[:,10], chirpL.t_b)
chirpL.plot1d(chirpL.results[:,10], chirpL.t_b)

# %% Barker 13, 1MHz

bark1 = signal("signal_data/barker_1MHz_13/signalbarker13.dat",
               "signal_data/barker_1MHz_13/bscanbarker13.dat")

bark1.plot1d()
bark1.plot2d(MIN=0, MAX=0.2)
bark1.plot2d(bark1.results, MIN=0, MAX=0.4)
bark1.plot1d(bark1.data_b[:,10], bark1.t_b)
bark1.plot1d(bark1.results[:,10], bark1.t_b)
