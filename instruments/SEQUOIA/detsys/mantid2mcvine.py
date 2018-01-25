#!/usr/bin/env python

from instrument.factories.SEQUOIA.Bootstrap_mantid_idf import *

f = 'SEQ_IDF_v2.xml'
factory = InstrumentFactory()
instrument, geometer = factory.construct(f)

# End of file 
