# $Id$
##
##  This file is part of pyFormex 0.8.9  (Fri Nov  9 10:49:51 CET 2012)
##  pyFormex is a tool for generating, manipulating and transforming 3D
##  geometrical models by sequences of mathematical operations.
##  Home page: http://pyformex.org
##  Project page:  http://savannah.nongnu.org/projects/pyformex/
##  Copyright 2004-2012 (C) Benedict Verhegghe (benedict.verhegghe@ugent.be) 
##  Distributed under the GNU General Public License version 3 or later.
##
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see http://www.gnu.org/licenses/.
##

"""Isoparametric transformations

"""
from __future__ import print_function

from coords import *


def evaluate(atoms,x,y=0,z=0):
    """Build a matrix of functions of coords.

    - `atoms`: a list of text strings representing a mathematical function of
      `x`, and possibly of `y` and `z`.
    - `x`, `y`, `z`: a list of x- (and optionally y-, z-) values at which the
      `atoms` will be evaluated. The lists should have the same length.

    Returns a matrix with `nvalues` rows and `natoms` colums.
    """
    aa = zeros((len(x),len(atoms)),Float)
    for k,a in enumerate(atoms):
        aa[:,k] = eval(a)
    return aa   


class Isopar(object):
    """A class representing an isoparametric transformation

        type is one of the keys in Isopar.isodata
        coords and oldcoords can be either arrays, Coords or Formex instances,
        but should be of equal shape, and match the number of atoms in the
        specified transformation type

    The following three formulations are equivalent ::

       trf = Isopar(eltype,coords,oldcoords)
       G = F.isopar(trf)

       trf = Isopar(eltype,coords,oldcoords)
       G = trf.transform(F)

       G = isopar(F,eltype,coords,oldcoords)

    """

    # REM: we should create a function to produce these data

    # LAGRANGIAN : 1,2,3 dim (LINE, QUAD, HEX)
    # TRIANGLE : 2,3 dim (TRI,TET)
    # SERENDIPITY : list ???

    # lagrangian(nx,ny,nz)
    #                type   ndim   degree+1
    #  'line2': ('lagrangian',1,(1))
    #  'quad9': ('lagrangian',2,(2,2))
    #  'quad6': ('lagrangian',2,(3,2))
    #  'quad6': 'lag-2-3-2'
    #  'quad8' : ('direct', 2, ('1','x','y','x*x','y*y','x*y','x*x*y','x*y*y')),
    #
    # generic name:
    #
    #   'lag-2-2-3' : ('lagrangian',2,(2,3))
    #   'tri-2-2' : ('triangular',2,(2))

    #   'lag-i-j-k' 
    
    
    isodata = {
        'line2' : (1, ('1','x')),
        'line3' : (1, ('1','x','x*x')),
        'line4' : (1, ('1','x','x**2','x**3')),
        'tri3'  : (2, ('1','x','y')),
        'tri3'  : (2, ('1','x','y')),
        'tri6'  : (2, ('1','x','y','x*x','y*y','x*y')),
        'quad4' : (2, ('1','x','y','x*y')),
        'quad8' : (2, ('1','x','y','x*x','y*y','x*y','x*x*y','x*y*y')),
        'quad9' : (2, ('1','x','y','x*x','y*y','x*y','x*x*y','x*y*y',
                       'x*x*y*y')),
        'quad13': (2, ('1','x','y','x*x','x*y','y*y',
                       'x*x*x','x*x*y','x*y*y','y*y*y',
                       'x*x*x*y','x*x*y*y','x*y*y*y')),
        'quad16': (2, ('1','x','y','x*x','x*y','y*y',
                       'x*x*x','x*x*y','x*y*y','y*y*y',
                       'x*x*x*y','x*x*y*y','x*y*y*y',
                       'x*x*x*y*y','x*x*y*y*y','x*x*x*y*y*y')),
        'tet4'  : (3, ('1','x','y','z')),
        'tet10' : (3, ('1','x','y','z','x*x','y*y','z*z','x*y','x*z','y*z')),
        'hex8'  : (3, ('1','x','y','z','x*y','x*z','y*z','x*y*z')),
        'hex20' : (3, ('1','x','y','z','x*x','y*y','z*z','x*y','x*z','y*z',
                       'x*x*y','x*x*z','x*y*y','y*y*z','x*z*z','y*z*z','x*y*z',
                       'x*x*y*z','x*y*y*z','x*y*z*z')),
        'hex27' : (3, ('1','x','y','z','x*x','y*y','z*z','x*y','x*z','y*z',
                       'x*x*y','x*x*z','x*y*y','y*y*z','x*z*z','y*z*z','x*y*z',
                       'x*x*y*y','x*x*z*z','y*y*z*z','x*x*y*z','x*y*y*z',
                       'x*y*z*z',
                       'x*x*y*y*z','x*x*y*z*z','x*y*y*z*z',
                       'x*x*y*y*z*z')),
        # quadratic in x,y, cubic in z
        'hex36' : (3, ('1','x','y','z','x*x','y*y','z*z','x*y','x*z','y*z',
                       'x*x*y','x*x*z','x*y*y','y*y*z','x*z*z','y*z*z','x*y*z',
                       'x*x*y*y','x*x*z*z','y*y*z*z','x*x*y*z','x*y*y*z',
                       'x*y*z*z',
                       'x*x*y*y*z','x*x*y*z*z','x*y*y*z*z',
                       'x*x*y*y*z*z',
                       'z*z*z','x*z*z*z','y*z*z*z',
                       'x*x*z*z*z','y*y*z*z*z','x*y*z*z*z',
                       'x*x*y*z*z*z','x*y*y*z*z*z','x*x*y*y*z*z*z')),
        'hex64': (3, ('1','x','y','z','x*x','y*y','z*z','x*y','x*z','y*z',
                      'x*x*y','x*x*z','x*y*y','y*y*z','x*z*z','y*z*z','x*y*z',
                      'x*x*x','y*y*y','z*z*z',
                      'x*x*y*y','x*x*z*z','y*y*z*z','x*x*y*z','x*y*y*z',
                      'x*y*z*z','x*x*x*y','x*x*x*z','x*y*y*y','y*y*y*z',
                      'x*z*z*z','y*z*z*z',
                      'x*x*x*y*y','x*x*x*z*z','x*x*y*y*y','y*y*y*z*z',
                      'z*z*z*x*x','z*z*z*y*y',
                      'x*x*x*y*z','x*y*y*y*z','z*z*z*x*y',
                      'x*x*y*y*z','x*x*y*z*z','x*y*y*z*z',
                      'x*x*x*y*y*y','x*x*x*z*z*z','y*y*y*z*z*z',
                      'x*x*x*y*y*z','x*x*x*y*z*z','y*y*y*x*x*z','y*y*y*x*z*z',
                      'z*z*z*x*x*y','z*z*z*x*y*y','x*x*y*y*z*z',
                      'x*x*x*y*y*y*z','x*x*x*y*z*z*z','y*y*y*x*z*z*z',
                      'x*x*x*y*y*z*z','y*y*y*x*x*z*z','z*z*z*x*x*y*y',
                      'x*x*x*y*y*y*z*z','x*x*x*z*z*z*y*y','y*y*y*z*z*z*x*x',
                      'x*x*x*y*y*y*z*z*z')),
        }


    def __init__(self,eltype,coords,oldcoords):
        """Create an isoparametric transformation.
        """
        ndim,atoms = Isopar.isodata[eltype]
        coords = coords.view().reshape(-1,3)
        oldcoords = oldcoords.view().reshape(-1,3)
        x = oldcoords[:,0]
        if ndim > 1:
            y = oldcoords[:,1]
        else:
            y = 0
        if ndim > 2:
            z = oldcoords[:,2]
        else:
            z = 0
        aa = evaluate(atoms,x,y,z)
        ab = linalg.solve(aa,coords)
        self.eltype = eltype
        self.trf = ab


    def transform(self,X):
        """Apply isoparametric transform to a set of coordinates.

        Returns a Coords array with same shape as X
        """
        if not isinstance(X,Coords):
            try:
                X = Coords(X)
            except:
                raise ValueError,"Expected a Coords object as argument"
        
        ndim,atoms = Isopar.isodata[self.eltype]
        aa = evaluate(atoms,X.x().ravel(),X.y().ravel(),X.z().ravel())
        xx = dot(aa,self.trf).reshape(X.shape)
        if ndim < 3:
            xx[...,ndim:] += X[...,ndim:]
        return X.__class__(xx)


# End
