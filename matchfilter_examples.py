#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 23:06:59 2022

@author: felixdubicki-piper
"""
from compress import signal
import numpy as np

x = 10  # slice to plot in 1D

# %% CLEAN U.S. PULSE, 2MHz

pulse = signal("signal_data/pulse_2MHznonoise/pulse2mhz.dat",
               "signal_data/pulse_2MHznonoise/bscan.dat")
title = r'Clean U.S. Pulse, $2\,$MHz'

plots = pulse.filter_example(filter_method=21, title=title, x=x, MAX=0.06)

# %% U.S. PULSE, 1MHz

pulse1 = signal("signal_data/pulse_1MHznoise/pulse1mhz.dat",
                "signal_data/pulse_1MHznoise/bscanpulse1.dat")
title = r'U.S. Pulse, $1\,$MHz'

plots = pulse1.filter_example(filter_method=21, title=title, x=x)

# %% U.S. PULSE, 2MHz

pulse2 = signal("signal_data/pulse_2MHznoise/pulse2mhz.dat",
                "signal_data/pulse_2MHznoise/bscanpulse2.dat")
title = r'U.S. Pulse, $2\,$MHz'

plots = pulse2.filter_example(filter_method=21, title=title, trim=80, x=x)

# %% Short Chirp, 0.8-2.2MHz

chirpS = signal("signal_data/chirp_0822MHz_2u/chirpsignal.dat",
                "signal_data/chirp_0822MHz_2u/bscanchirp0822.dat")
title = r'Chirp Pulse, $0.8\,$-$\,2.2\,$MHz, $2\,\mu$s'

plots = chirpS.filter_example(filter_method=21, title=title, trim=100, x=x)

# %% Long Chirp, 0.8-2.2MHz

chirpL = signal("signal_data/chirp_0822MHz_6u/longchirp.dat",
                "signal_data/chirp_0822MHz_6u/bscan.dat")
title = r'Chirp Pulse, $0.8\,$-$\,2.2\,$MHz, $6\,\mu$s'

plots = chirpL.filter_example(filter_method=21, title=title, trim=-45, x=x)

# %% Barker 13, 1MHz

bark1 = signal("signal_data/barker_1MHz_13/signalbarker13.dat",
               "signal_data/barker_1MHz_13/bscanbarker13.dat")
title = r'Barker Code (length $13$), $1\,$MHz'

plots = bark1.filter_example(filter_method=21, title=title, trim=-300, x=x,
                             remove_matchedpulse=700)

# %% Barker 13, 2MHz

bark2 = signal("signal_data/barker_2MHz_13/barker13.dat",
               "signal_data/barker_2MHz_13/bscanbarker13.dat")
title = r'Barker Code (length $13$), $1\,$MHz'

plots = bark2.filter_example(filter_method=21, title=title, x=x)

# %% Golay 3, 2MHz

gtrim = 100
gfilt = 21

# MAIN SIGNAL

golay = signal("signal_data/golay/golay_a_l3_2.dat",
               "signal_data/golay/bscangolay2mhz_l3nc.dat")
title = r'Golay Code (length $3$), $2\,$MHz'

plots = golay.filter_example(filter_method=gfilt, trim=gtrim,
                             title=title, x=x,
                             plotresults=(0, 0, 0, 0, 0))

# COMPLEMENTARY SIGNAL

golayC = signal("signal_data/golay/golay_l3_2c.dat",
                "signal_data/golay/bscangolay2mhz_l3c.dat")
title = r'Golay Complementary Code (length $3$), $2\,$MHz'

plotsC = golayC.filter_example(filter_method=gfilt, trim=gtrim,
                               title=title, x=x,
                               plotresults=(0, 0, 0, 0, 0))

# SUM OF FILTERED SIGNALS

golay_sum = signal("signal_data/golay/golay_a_l3_2.dat",
                   "signal_data/golay/bscangolay2mhz_l3nc.dat")
title = r'Golay Code (length $3$), $2\,$MHz'

golay_sum.results = golay.results + golayC.results

plotsS = golay_sum.filter_example(signal=golay_sum.results,
                                  filter_method=0, remove_pulse=0,
                                  title=title, x=x,
                                  plotresults=(1, 1, 1, 1, 1))
