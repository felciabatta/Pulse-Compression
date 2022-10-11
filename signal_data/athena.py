#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np


def ReadAScan(filename):
    fid = open(filename, mode="r")

    line = fid.readline().strip()
    # Originally said 'Version 2.1' but all A-Scan files were 2.0
    if line != "#Milena A-Scan result file               Version 2.0":
        print("ReadAScan: unsupported file format")
        fid.close()
        return None, None

    # get n. iterations, timestep, t0
    # note that nit do not include t0, whereas for the B-Scan, it does
    # note *1e6 to account for unit error in data
    nit, dt, t0, _ = fid.readline().split()
    nit, dt, t0 = int(nit), float(dt)*1e6, float(t0)/1e9

    # extract data
    data = np.array([float(l) for l in fid.readlines()])

    # convert iterations to time series
    t = np.arange(0, nit+1, 1)*dt
    # t = np.arange(t0, t0+len(data)*dt, dt) # original, equivalent

    fid.close()

    return t, data


def ReadBScan(filename):
    fid = open(filename, mode="r")

    line = fid.readline().strip()
    if line != "#BSCAN format 2D":
        print("ReadBScan: unsupported file format")
        fid.close()
        return None, None, None

    # get n. x & t iterations
    # note that nit includes t0, whereas for the A-Scan, it does not
    nix, nit, _ = fid.readline().split()
    nix, nit = int(nix), int(nit)

    # time & x step
    dx, _, dt = fid.readline().split()
    dx, dt = float(dx), float(dt)*1e-6

    # extract data
    data = np.array([float(l)
                     for l in fid.readlines()]).reshape((nit, nix))

    # convert iterations to time & x series
    t = np.arange(0, nit, 1)*dt
    x = np.arange(0, nix, 1)*dx

    fid.close()

    return t, x, data
