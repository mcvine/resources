#!/usr/bin/env python

"""
compute phase (degree) of fermi chopper at t=0
"""


Ei = 686.62
width = 2.54e-2 * .5

from mcni.utils import conversion as Conv
vi = Conv.e2v(Ei)

t = width / vi * 1e6
print t
