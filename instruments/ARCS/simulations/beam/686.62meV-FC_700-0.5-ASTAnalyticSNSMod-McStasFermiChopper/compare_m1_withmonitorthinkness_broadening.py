#!/usr/bin/env python
import histogram.hdf as hh, os

# exp = hh.load(os.path.expanduser("/SNS/users/linjiao/simulations/ARCS/He4/2015/exp/11315/m2-focused.h5"))
exp = hh.load(os.path.expanduser("/SNS/users/linjiao/simulations/ARCS/mod2sample/686.62meV/exp/m1-focused.h5"))
sim = hh.load("out/mon1-itof-focused.h5")
oldsim = hh.load("../../fitmonitor/n1e9/out/mon1-itof-focused.h5")

tofmin, tofmax = 1021, 1055

us = 1.e-6

exp = exp[(tofmin, tofmax)]
sim = sim[(tofmin*us, tofmax*us)]
oldsim = oldsim[(tofmin*us, tofmax*us)]

from convolve import convolve
sim2I = convolve(sim, 1.1*us, N=20)

import pylab
pylab.plot(exp.tof, exp.I, label="exp")
# pylab.plot(sim.tof*1e6+3, sim.I*.000031, label="sim")
# pylab.plot(sim.tof/us-.7, sim.I*.78, label="sim")
# pylab.plot(sim.tof/us-.7, sim2I*.85, label="sim with monitor thickness effect")
pylab.plot(sim.tof/us-.7, sim2I*.85, label="sim")
pylab.plot(oldsim.tof/us+3.1, oldsim.I*.49, label="old sim")

pylab.xlim(1020, 1055)
pylab.legend()
pylab.show()
