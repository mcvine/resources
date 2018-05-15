# create an xml file that includes all shapes in the MICAS furnace

import numpy as np
from instrument.geometry.pml import weave
from instrument.geometry import shapes, operations

def hollowCylinder(in_radius, out_radius, height):
    h, unit = height.split('*')
    h = float(h)
    inner_h = '%s*%s' % (h*1.1, unit)
    return operations.subtract(shapes.cylinder(radius=out_radius, height=height), shapes.cylinder(radius=in_radius, height=inner_h))

block = shapes.block(width="6*cm", height="10*cm", thickness="0.5*mm")
outmost = hollowCylinder(in_radius="7.75*inch", out_radius="7.75*inch+0.25*mm", height="15*inch")
subcomps = [block, outmost]

subcomps.append(hollowCylinder(in_radius="3.5*cm", out_radius="3.5*cm+0.25*mm", height="15*inch"))
subcomps.append(hollowCylinder(in_radius="3.55*cm", out_radius="3.55*cm+0.25*mm", height="15*inch"))
subcomps.append(hollowCylinder(in_radius="6.0*cm", out_radius="6.0*cm+0.25*mm", height="15*inch"))
subcomps.append(hollowCylinder(in_radius="6.5*cm", out_radius="6.5*cm+0.25*mm", height="15*inch"))
subcomps.append(hollowCylinder(in_radius="7.0*cm", out_radius="7.0*cm+0.25*mm", height="15*inch"))
subcomps.append(hollowCylinder(in_radius="7.5*cm", out_radius="7.5*cm+0.25*mm", height="15*inch"))
subcomps.append(hollowCylinder(in_radius="8.0*cm", out_radius="8.0*cm+0.25*mm", height="15*inch"))
subcomps.append(hollowCylinder(in_radius="8.5*cm", out_radius="8.5*cm+0.25*mm", height="15*inch"))
subcomps.append(hollowCylinder(in_radius="9.0*cm", out_radius="9.0*cm+0.25*mm", height="15*inch"))
subcomps.append(hollowCylinder(in_radius="9.5*cm", out_radius="9.5*cm+0.25*mm", height="15*inch"))

shape = operations.unite(*subcomps)
text = weave(shape, open('shape.xml', 'wt'), print_docs = False )
