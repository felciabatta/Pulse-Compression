#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 23:06:59 2022

@author: felixdubicki-piper
"""
from compress import signal
import numpy as np

x = 10  # slice to plot in 1D
filter_methods = [1, 2, 12, 21]
# fm = 2

# %% LOOP Everything
allSNR = []
allSNRs = []
allMaxCoords = []
allPSR = []
allPSRs = []
allRangeRsn = []
allRangeRsns = []
for i, fm in enumerate(filter_methods):
    # %% CLEAN U.S. PULSE, 2MHz

    pulse = signal("signal_data/pulse_2MHznonoise/pulse2mhz.dat",
                   "signal_data/pulse_2MHznonoise/bscan.dat")
    title = r'Clean U.S. Pulse, $2\,$MHz'

    plots = pulse.filter_example(filter_method=fm, title=title, x=x, MAX=0.06)

    # %% U.S. PULSE, 1MHz

    pulse1 = signal("signal_data/pulse_1MHznoise/pulse1mhz.dat",
                    "signal_data/pulse_1MHznoise/bscanpulse1.dat")
    title = r'U.S. Pulse, $1\,$MHz'

    plots = pulse1.filter_example(filter_method=fm, title=title, x=x)
    maxCoords_p1, SNRs_p1, SNR_p1 = pulse1.SNR_example(
        [550, 10], plots, plotMyGuess=1, window=np.array([40, 3]))
    PSRs_p1, PSR_p1 = pulse1.peakSidelobeRatio()
    defectWidths_p1, defectWidth_p1 = pulse1.peakWidths()

    # %% U.S. PULSE, 2MHz

    pulse2 = signal("signal_data/pulse_2MHznoise/pulse2mhz.dat",
                    "signal_data/pulse_2MHznoise/bscanpulse2.dat")
    title = r'U.S. Pulse, $2\,$MHz'

    plots = pulse2.filter_example(filter_method=fm, title=title, trim=80, x=x)
    maxCoords_p2, SNRs_p2, SNR_p2 = pulse2.SNR_example(
        [450, 10], plots, plotMyGuess=1, window=np.array([30, 2]), trim=80)
    PSRs_p2, PSR_p2 = pulse2.peakSidelobeRatio()
    defectWidths_p2, defectWidth_p2 = pulse2.peakWidths()

    # %% Short Chirp, 0.8-2.2MHz

    chirpS = signal("signal_data/chirp_0822MHz_2u/chirpsignal.dat",
                    "signal_data/chirp_0822MHz_2u/bscanchirp0822.dat")
    title = r'Chirp Pulse, $0.8\,$-$\,2.2\,$MHz, $2\,\mu$s'

    if fm == 2:
        # GUESS: use 350 for wien (2), 450 for everything else
        tguess = 350
    else:
        tguess = 450

    plots = chirpS.filter_example(filter_method=fm, title=title, trim=100, x=x)
    maxCoords_cS, SNRs_cS, SNR_cS = chirpS.SNR_example(
        [tguess, 10], plots, plotMyGuess=1, window=np.array([40, 3]), trim=100)
    PSRs_cS, PSR_cS = chirpS.peakSidelobeRatio()
    defectWidths_cS, defectWidth_cS = chirpS.peakWidths()

    # %% Long Chirp, 0.8-2.2MHz

    chirpL = signal("signal_data/chirp_0822MHz_6u/longchirp.dat",
                    "signal_data/chirp_0822MHz_6u/bscan.dat")
    title = r'Chirp Pulse, $0.8\,$-$\,2.2\,$MHz, $6\,\mu$s'

    plots = chirpL.filter_example(filter_method=fm, title=title, trim=-45, x=x)
    maxCoords_cL, SNRs_cL, SNR_cL = chirpL.SNR_example([550, 10], plots, plotMyGuess=1,
                                                       window=np.array([40, 3]), trim=-45)
    PSRs_cL, PSR_cL = chirpL.peakSidelobeRatio()
    defectWidths_cL, defectWidth_cL = chirpL.peakWidths()

    # %% Barker 13, 1MHz

    bark1 = signal("signal_data/barker_1MHz_13/signalbarker13.dat",
                   "signal_data/barker_1MHz_13/bscanbarker13.dat")
    title = r'Barker Code (length $13$), $1\,$MHz'

    if fm == 2:
        # GUESS: use 1000 for wien (2), 800 for everything else
        tguess = 1000
        SNRtrim = 0
    else:
        tguess = 800
        SNRtrim = -300

    plots = bark1.filter_example(filter_method=fm, title=title, trim=-300, x=x,
                                 remove_matchedpulse=700)
    maxCoords_b1, SNRs_b1, SNR_b1 = bark1.SNR_example([tguess, 10], plots, plotMyGuess=1,
                                                      window=np.array([40, 3]), trim=SNRtrim)
    PSRs_b1, PSR_b1 = bark1.peakSidelobeRatio()
    defectWidths_b1, defectWidth_b1 = bark1.peakWidths()

    # %% Barker 13, 2MHz

    bark2 = signal("signal_data/barker_2MHz_13/barker13.dat",
                   "signal_data/barker_2MHz_13/bscanbarker13.dat")
    title = r'Barker Code (length $13$), $1\,$MHz'

    plots = bark2.filter_example(filter_method=fm, title=title, x=40)
    maxCoords_b2, SNRs_b2, SNR_b2 = bark2.SNR_example([575, 10], plots, plotMyGuess=1,
                                                      window=np.array([40, 3]))
    PSRs_b2, PSR_b2 = bark2.peakSidelobeRatio()
    defectWidths_b2, defectWidth_b2 = bark2.peakWidths()

    if 0:
        window = 5
        T = bark2.data_b.shape[0]
        N = bark2.data_b.shape[1] // window
        R = bark2.data_b.shape[1] % window
        prodarray = np.zeros((T, N))
        for n in range(N):
            x0 = n*window
            xend = (n+1)*window
            prodarray[:, n] = np.prod(bark2.results[:, x0:xend], 1)
            prodarray[:, n] /= max(prodarray[:1700, n])

        bark2.plot2d(prodarray, MIN=0.8, MAX=0.9)
        bark2.plot1d(prodarray[:, 2], t=bark2.t_b)

        window = 1
        T = bark2.data_b.shape[0]
        N = bark2.data_b.shape[1] - 2*window
        R = 2*window
        prodarray = np.zeros((T, N))
        for n in range(N):
            x0 = n
            xend = n+2*window+1
            prodarray[:, n] = np.prod(bark2.results[:, x0:xend], 1)
            prodarray[:, n] /= max(prodarray[:1700, n])
            # prodarray[:, n] = np.log(abs(prodarray[:, n]))*np.sign(prodarray[:, n])

        bark2.plot2d(prodarray, MIN=0, MAX=1)
        # for n in range(N):
        #     bark2.plot1d(prodarray[:, n], t=bark2.t_b, ylim=(0, 1))

    # %% Golay 3, 2MHz

    gtrim = 100
    if fm == 12:
        gfilt1 = 1
        gfilt2 = 2
    else:
        gfilt1 = fm
        gfilt2 = 0

    # MAIN SIGNAL

    golay = signal("signal_data/golay/golay_a_l3_2.dat",
                   "signal_data/golay/bscangolay2mhz_l3nc.dat")
    title = r'Golay Code (length $3$), $2\,$MHz'

    plots = golay.filter_example(filter_method=gfilt1, trim=gtrim,
                                 title=title, x=x,
                                 plotresults=(0, 0, 0, 0, 0))

    # COMPLEMENTARY SIGNAL

    golayC = signal("signal_data/golay/golay_l3_2c.dat",
                    "signal_data/golay/bscangolay2mhz_l3c.dat")
    title = r'Golay Complementary Code (length $3$), $2\,$MHz'

    plotsC = golayC.filter_example(filter_method=gfilt1, trim=gtrim,
                                   title=title, x=x,
                                   plotresults=(0, 0, 0, 0, 0))

    # SUM OF FILTERED SIGNALS

    golay_sum = signal("signal_data/golay/golay_a_l3_2.dat",
                       "signal_data/golay/bscangolay2mhz_l3nc.dat")
    title = r'Golay Code (length $3$), $2\,$MHz'

    golay_sum.results = golay.results + golayC.results

    plotsS = golay_sum.filter_example(signal=golay_sum.results,
                                      filter_method=gfilt2, remove_pulse=0,
                                      title=title, x=x,
                                      plotresults=(1, 1, 1, 1, 1))

    maxCoords_gS, SNRs_gS, SNR_gS = golay_sum.SNR_example([500, 10], plotsS, plotMyGuess=1,
                                                          window=np.array([40, 3]), trim=100)
    PSRs_gS, PSR_gS = golay_sum.peakSidelobeRatio()
    defectWidths_gS, defectWidth_gS = golay_sum.peakWidths()


# %% COMPILE Current Stats

    allSNR.append(((SNR_b1),
                   (SNR_b2),
                   (SNR_cS),
                   (SNR_cL),
                   (SNR_gS),
                   (SNR_p1),
                   (SNR_p2)))
    allSNRs.append(((SNRs_b1),
                    (SNRs_b2),
                    (SNRs_cS),
                    (SNRs_cL),
                    (SNRs_gS),
                    (SNRs_p1),
                    (SNRs_p2)))
    allMaxCoords.append(((maxCoords_b1),
                         (maxCoords_b2),
                         (maxCoords_cS),
                         (maxCoords_cL),
                         (maxCoords_gS),
                         (maxCoords_p1),
                         (maxCoords_p2)))
    allRangeRsn.append(((defectWidth_b1),
                        (defectWidth_b2),
                        (defectWidth_cS),
                        (defectWidth_cL),
                        (defectWidth_gS),
                        (defectWidth_p1),
                        (defectWidth_p2)))
    allRangeRsns.append(((defectWidths_b1),
                         (defectWidths_b2),
                         (defectWidths_cS),
                         (defectWidths_cL),
                         (defectWidths_gS),
                         (defectWidths_p1),
                         (defectWidths_p2)))
    allPSR.append(((PSR_b1),
                   (PSR_b2),
                   (PSR_cS),
                   (PSR_cL),
                   (PSR_gS),
                   (PSR_p1),
                   (PSR_p2)))
    allPSRs.append(((PSRs_b1),
                    (PSRs_b2),
                    (PSRs_cS),
                    (PSRs_cL),
                    (PSRs_gS),
                    (PSRs_p1),
                    (PSRs_p2)))

# %% COMPILE all Stats
allSNR = np.array(allSNR).transpose()
allSNRs = np.concatenate(allSNRs, 1)

allMaxTCoords = np.concatenate(allMaxCoords, 1)[:, :, 0]
allMaxXCoords = np.concatenate(allMaxCoords, 1)[:, :, 1]

allPSR = np.array(allPSR).transpose()
allPSRs = np.concatenate(allPSRs, 1)

allRangeRsn = np.array(allRangeRsn).transpose()
allRangeRsns = np.concatenate(allRangeRsns, 1)


if 0:
    np.savetxt('Results/Mean-TrueSNR.csv', allSNR, delimiter=',')
    np.savetxt('Results/Defect-TrueSNR.csv', allSNRs, delimiter=',')

    np.savetxt('Results/Defect-TCoords.csv', allMaxTCoords, delimiter=',')
    np.savetxt('Results/Defect-XCoords.csv', allMaxXCoords, delimiter=',')

    np.savetxt('Results/Mean-PSR.csv', allPSR, delimiter=',')
    np.savetxt('Results/Defect-PSR.csv', allPSRs, delimiter=',')

    np.savetxt('Results/Mean-RangeRSN.csv', allPSR, delimiter=',')
    np.savetxt('Results/Defect-RangeRSN.csv', allPSRs, delimiter=',')
