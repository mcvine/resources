#!/usr/bin/env python

"""convolve monitor data with a rectangle function
to simulate the width effect of the monitor
"""

import numpy as np

def convolve(m, width, N=10):
    tof = m.tof
    start = tof[0]; end = tof[-1]
    Dt = tof[1]-tof[0]
    dt = Dt/N
    finertof = np.arange(start-Dt/2., end+Dt/2., dt)
    y = np.interp(finertof, tof, m.I) / N
    k = np.ones(int(width/dt))
    k/=k.size
    conved = np.convolve(y, k, mode='same')
    conved.shape = -1, N
    return np.sum(conved, -1)
