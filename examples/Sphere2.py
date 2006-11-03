#!/usr/bin/env pyformex
# $Id$
#
"""Sphere2"""

from simple import Sphere2,Sphere3

nx = 4
ny = 4
m = 1.6
ns = 6
smooth()
for i in range(ns):
    b = Sphere2(nx,ny,bot=-90,top=90).translate1(0,-1.0)
    s = Sphere3(nx,ny,bot=-90,top=90).translate1(0,1.0)
    s.setProp(3)
    clear()
    bb = bbox([b,s])
    draw(b,bbox=bb,view='front',wait=False)
    draw(s,bbox=bb,view='front')
    nx = int(m*nx)
    ny = int(m*ny)
