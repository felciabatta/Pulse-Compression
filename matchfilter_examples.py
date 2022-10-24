#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 23:06:59 2022

@author: felixdubicki-piper
"""

from compress import *
x = 10  # slice to plot in 1D

# %% CLEAN U.S. PULSE, 2MHz

pulse = signal("signal_data/pulse_2MHznonoise/pulse2mhz.dat",
               "signal_data/pulse_2MHznonoise/bscan.dat")
title = r'Clean U.S. Pulse, $2\,$MHz'

pulse.match2d(remove_pulse=1)

plot = pulse.plot1d(title=title)

plotbf = pulse.plot1d(pulse.data_b[:, x], pulse.t_b, title=title)
plotaf = pulse.plot1d(pulse.results[:, x], pulse.t_b, title=title)

mapbf = pulse.plot2d(MIN=0, MAX=0.04, title=title)
mapaf = pulse.plot2d(pulse.results, MIN=0, MAX=0.04, title=title)


# %% U.S. PULSE, 1MHz

pulse1 = signal("signal_data/pulse_1MHznoise/pulse1mhz.dat",
                "signal_data/pulse_1MHznoise/bscanpulse1.dat")
title = r'U.S. Pulse, $1\,$MHz'

pulse1.match2d(remove_pulse=1)
pulse1.wien(window=(100, 10))

plot = pulse1.plot1d(title=title)

plotbf = pulse1.plot1d(pulse1.data_b[:, x], pulse1.t_b, title=title)
plotaf = pulse1.plot1d(pulse1.results[:, x], pulse1.t_b, title=title)

mapbf = pulse1.plot2d(MIN=0, MAX=0.08, title=title)
mapaf = pulse1.plot2d(pulse1.results, MIN=0, MAX=0.08, title=title)


# %% U.S. PULSE, 2MHz

pulse2 = signal("signal_data/pulse_2MHznoise/pulse2mhz.dat",
                "signal_data/pulse_2MHznoise/bscanpulse2.dat")
title = r'U.S. Pulse, $2\,$MHz'

pulse2.match2d(remove_pulse=1, trim=80)
# pulse2.wien(window=(100, 10))

plot = pulse2.plot1d(title=title)

plotbf = pulse2.plot1d(pulse2.data_b[:, x], pulse2.t_b, title=title)
plotaf = pulse2.plot1d(pulse2.results[:, x], pulse2.t_b, title=title)

mapbf = pulse2.plot2d(MIN=0, MAX=0.02, title=title)
mapaf = pulse2.plot2d(pulse2.results, MIN=0, MAX=0.02, title=title)


# %% Short Chirp, 0.8-2.2MHz

chirpS = signal("signal_data/chirp_0822MHz_2u/chirpsignal.dat",
                "signal_data/chirp_0822MHz_2u/bscanchirp0822.dat")
title = r'Chirp Pulse, $0.8\,$-$\,2.2\,$MHz, $2\,\mu$s'

chirpS.match2d(remove_pulse=1, trim=100)
# chirpS.wien(window=(100, 10))

plot = chirpS.plot1d(title=title)
x=0
plotbf = chirpS.plot1d(chirpS.data_b[:, x], chirpS.t_b, title=title)
plotaf = chirpS.plot1d(chirpS.results[:, x], chirpS.t_b, title=title)

mapbf = chirpS.plot2d(MIN=0, MAX=0.08, title=title)
mapaf = chirpS.plot2d(chirpS.results, MIN=0, MAX=0.2, title=title)


# %% Long Chirp, 0.8-2.2MHz

chirpL = signal("signal_data/chirp_0822MHz_6u/longchirp.dat",
                "signal_data/chirp_0822MHz_6u/bscan.dat")
title = r'Chirp Pulse, $0.8\,$-$\,2.2\,$MHz, $6\,\mu$s'

chirpL.match2d(remove_pulse=1, trim=-45)
chirpL.wien(window=(100,10))

plot = chirpL.plot1d(title=title)

plotbf = chirpL.plot1d(chirpL.data_b[:, x], chirpL.t_b, title=title)
plotaf = chirpL.plot1d(chirpL.results[:, x], chirpL.t_b, title=title)

mapbf = chirpL.plot2d(MIN=0, MAX=0.08, title=title)
mapaf = chirpL.plot2d(chirpL.results, MIN=0, MAX=0.2, title=title)


# %% Barker 13, 1MHz

bark1 = signal("signal_data/barker_1MHz_13/signalbarker13.dat",
               "signal_data/barker_1MHz_13/bscanbarker13.dat")
title = r'Barker Code (length $13$), $1\,$MHz'

bark1.match2d(remove_pulse=1, trim=-300)
# bark1.results[:700,:]=np.mean(abs(bark1.results[701:,:]))
bark1.results[:700, :] = 0
bark1.wien(window=(100, 10))

plot = bark1.plot1d(title=title)

plotbf = bark1.plot1d(bark1.data_b[:, x], bark1.t_b, title=title)
plotaf = bark1.plot1d(bark1.results[:, x], bark1.t_b, title=title)

mapbf = bark1.plot2d(MIN=0, MAX=0.2, title=title)
mapaf = bark1.plot2d(bark1.results, MIN=0, MAX=0.4, title=title)


# %% Barker 13, 2MHz

bark2 = signal("signal_data/barker_2MHz_13/barker13.dat",
               "signal_data/barker_2MHz_13/bscanbarker13.dat")
title = r'Barker Code (length $13$), $1\,$MHz'

bark2.match2d(remove_pulse=1)
bark2.wien(window=(100, 10))

plot = bark2.plot1d(title=title)

plotbf = bark2.plot1d(bark2.data_b[:, x], bark2.t_b, title=title)
plotaf = bark2.plot1d(bark2.results[:, x], bark2.t_b, title=title)

mapbf = bark2.plot2d(MIN=0, MAX=0.2, title=title)
mapaf = bark2.plot2d(bark2.results, MIN=0.0, MAX=0.10, title=title)


# %% Golay 3, 2MHz

# ~~~~~~~~~~~
# MAIN SIGNAL
# ~~~~~~~~~~~

golay = signal("signal_data/golay/golay_a_l3_2.dat",
               "signal_data/golay/bscangolay2mhz_l3nc.dat")
title = r'Golay Code (length $3$), $2\,$MHz'

gtrim = 100

golay.match2d(remove_pulse=1, trim=gtrim)
# golay.wien()

plot = golay.plot1d(title=title)
# plotbf = golay.plot1d(golay.data_b[:, x], golay.t_b,title=title)
# plotaf = golay.plot1d(golay.results[:, x], golay.t_b,title=title)

# mapbf = golay.plot2d(MIN=0, MAX=0.1, title=title)
# mapaf = golay.plot2d(golay.results, MIN=0, MAX=0.2,title=title)

# ~~~~~~~~~~~~~~~~~~~~
# COMPLEMENTARY SIGNAL
# ~~~~~~~~~~~~~~~~~~~~

golayC = signal("signal_data/golay/golay_l3_2c.dat",
                "signal_data/golay/bscangolay2mhz_l3c.dat")

golayC.match2d(remove_pulse=1, trim=gtrim)
# golayC.wien()

# plot = golayC.plot1d(title=title)
# plotbf = golayC.plot1d(golayC.data_b[:, x], golayC.t_b,title=title)
# plotaf = golayC.plot1d(golayC.results[:, x], golayC.t_b,title=title)

# mapbf = golayC.plot2d(MIN=0, MAX=0.1,title=title)
# mapaf = golayC.plot2d(golayC.results, MIN=0, MAX=0.2,title=title)

# ~~~~~~~~~~~~~~~~~~~~~~~
# SUM OF FILTERED SIGNALS
# ~~~~~~~~~~~~~~~~~~~~~~~

golay_sum = signal("signal_data/golay/golay_a_l3_2.dat",
                   "signal_data/golay/bscangolay2mhz_l3nc.dat")

golay_sum.results = golay.results + golayC.results
# golay_sum.results[-200:, :] = 0
golay_sum.wien(window=(100,10))
# golay_sum.results[-200:, :] = np.nan # HMMM?

plotbf = golay_sum.plot1d(golay.data_b[:, x], golay.t_b, title=title)
plotaf = golay_sum.plot1d(golay_sum.results[:, x], golay_sum.t_b, title=title)

mapbf = golay.plot2d(MIN=0, MAX=0.1, title=title)
mapaf = golay_sum.plot2d(golay_sum.results, MIN=0.0, MAX=0.2, title=title)
