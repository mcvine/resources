#!/usr/bin/env python

"""
compute phase (degree) of fermi chopper at t=0
"""


Ei = 686.62
freq = 600.
dist = 11.61 # mod to fc
t_emission = 3.8 * 1e-6


from mcni.utils import conversion as Conv
vi = Conv.e2v(Ei)


t_fc = dist/vi + t_emission
phase = -t_fc * freq * 360.
print phase
