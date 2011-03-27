# $Id$
##
##  This file is part of pyFormex 0.8.3 Release Sun Dec  5 18:01:17 2010
##  pyFormex is a tool for generating, manipulating and transforming 3D
##  geometrical models by sequences of mathematical operations.
##  Homepage: http://pyformex.org   (http://pyformex.berlios.de)
##  Copyright (C) Benedict Verhegghe (benedict.verhegghe@ugent.be) 
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
"""Basic OpenGL drawing functions.

The functions in this module should be exact emulations of the
external functions in the compiled library lib.drawgl.

These are low level functions that should normally not be used by
the user.
"""

# There should be no other imports here than OpenGL and numpy
from OpenGL import GL,GLU
from numpy import *

def get_version():
    return 0


def glColor(color,alpha=1.0):
    """Set the OpenGL color, possibly with transparency.

    color is a tuple of 3 real values.
    alpha is a single real value.
    All values are between 0.0 and 1.0
    """
    if alpha == 1.0:
        GL.glColor3fv(color)
    else:
        GL.glColor4fv(append(color,alpha)) 


def glObjType(nplex):
    if nplex == 1:
        objtype = GL.GL_POINTS
    elif nplex == 2:
        objtype = GL.GL_LINES
    elif nplex == 3:
        objtype = GL.GL_TRIANGLES
    elif nplex == 4:
        objtype = GL.GL_QUADS
    else:
        objtype = GL.GL_POLYGON
    return objtype


def draw_polygons(x,n,c,alpha,objtype):
    """Draw a collection of polygons.

    x : float (nel,nplex,3) : coordinates.
    n : float (nel,3) or (nel,nplex,3) : normals.
    c : float (nel,3) or (nel,nplex,3) : color(s)
    alpha : float
    objtype : GL Object type (-1 = auto)

    If nplex colors per element are given, and shading mode is flat,
    the last color will be used.
    """
    x = x.astype(float32)
    nplex = x.shape[1]
    if n is not None:
        n = n.astype(float32)
    if c is not None:
        c = c.astype(float32)
    if objtype < 0:
        objtype = glObjType(nplex)
        
    if nplex <= 4 and glObjType(nplex) == objtype:
        GL.glBegin(objtype)
        if c is None:
            if n is None:
                for xi in x.reshape((-1,3)):
                    GL.glVertex3fv(xi)
            elif n.ndim == 2:
                for xi,ni in zip(x,n):
                    GL.glNormal3fv(ni)
                    for j in range(nplex):
                        GL.glVertex3fv(xi[j])
            elif n.ndim == 3:
                for i in range(x.shape[0]):
                    for xij,nij in zip(x[i],n[i]):
                        GL.glNormal3fv(nij)
                        GL.glVertex3fv(xij)

        elif c.ndim == 2:
            if n is None:
                for xi,ci in zip(x,c):
                    GL.glColor3fv(ci)
                    for j in range(nplex):
                        GL.glVertex3fv(xi[j])
            elif n.ndim == 2:
                for xi,ni,ci in zip(x,n,c):
                    GL.glColor3fv(ci)
                    GL.glNormal3fv(ni)
                    for j in range(nplex):
                        GL.glVertex3fv(xi[j])
            elif n.ndim == 3:
                for xi,ni,ci in zip(x,n,c):
                    GL.glColor3fv(ci)
                    for j in range(nplex):
                        GL.glNormal3fv(ni[j])
                        GL.glVertex3fv(xi[j])

        elif c.ndim == 3:
            if n is None:
                for xi,ci in zip(x.reshape((-1,3)),c.reshape((-1,3))):
                    GL.glColor3fv(ci)
                    GL.glVertex3fv(xi)
            elif n.ndim == 2:
                for xi,ni,ci in zip(x,n,c):
                    GL.glNormal3fv(ni)
                    for j in range(nplex):
                        GL.glColor3fv(ci[j])
                        GL.glVertex3fv(xi[j])
            elif n.ndim == 3:
                for xi,ni,ci in zip(x.reshape((-1,3)),n.reshape((-1,3)),c.reshape((-1,3))):
                    GL.glColor3fv(ci)
                    GL.glNormal3fv(ni)
                    GL.glVertex3fv(xi)
        GL.glEnd()

    else:

        if c is None:
            if n is None:
                for xi in x:
                    GL.glBegin(objtype)
                    for j in range(nplex):
                        GL.glVertex3fv(xi[j])
                    GL.glEnd()
            elif n.ndim == 2:
                for xi,ni in zip(x,n):
                    GL.glBegin(objtype)
                    GL.glNormal3fv(ni)
                    for j in range(nplex):
                        GL.glVertex3fv(xi[j])
                    GL.glEnd()
            elif n.ndim == 3:
                for i in range(x.shape[0]):
                    GL.glBegin(objtype)
                    for xij,nij in zip(x[i],n[i]):
                        GL.glNormal3fv(nij)
                        GL.glVertex3fv(xij)
                    GL.glEnd()

        elif c.ndim == 2:
            if n is None:
                for xi,ci in zip(x,c):
                    GL.glBegin(objtype)
                    GL.glColor3fv(ci)
                    for j in range(nplex):
                        GL.glVertex3fv(xi[j])
                    GL.glEnd()
            elif n.ndim == 2:
                for xi,ni,ci in zip(x,n,c):
                    GL.glBegin(objtype)
                    GL.glColor3fv(ci)
                    GL.glNormal3fv(ni)
                    for j in range(nplex):
                        GL.glVertex3fv(xi[j])
                    GL.glEnd()
            elif n.ndim == 3:
                for xi,ni,ci in zip(x,n,c):
                    GL.glBegin(objtype)
                    GL.glColor3fv(ci)
                    for j in range(nplex):
                        GL.glNormal3fv(ni[j])
                        GL.glVertex3fv(xi[j])
                    GL.glEnd()

        elif c.ndim == 3:
            if n is None:
                for xi,ci in zip(x,c):
                    GL.glBegin(objtype)
                    GL.glColor3fv(ci)
                    for j in range(nplex):
                        GL.glColor3fv(ci[j])
                        GL.glVertex3fv(xi[j])
                    GL.glEnd()
            elif n.ndim == 2:
                for xi,ni,ci in zip(x,n,c):
                    GL.glBegin(objtype)
                    GL.glNormal3fv(ni)
                    for j in range(nplex):
                        GL.glColor3fv(ci[j])
                        GL.glVertex3fv(xi[j])
                    GL.glEnd()
            elif n.ndim == 3:
                for xi,ni,ci in zip(x,n,c):
                    GL.glBegin(objtype)
                    for j in range(nplex):
                        GL.glColor3fv(ci[j])
                        GL.glNormal3fv(ni[j])
                        GL.glVertex3fv(xi[j])
                    GL.glEnd()

        

def pick_polygons(x,objtype):
    """Mimics draw_polygons for picking purposes.

    x : float (nel,nplex,3) : coordinates.
    objtype : GL Object type (-1 = auto)
    """
    nplex = x.shape[1]

    if objtype < 0:
        objtype = glObjType(nplex)

    for i,xi in enumerate(x): 
        GL.glPushName(i)
        GL.glBegin(objtype)
        for xij in xi:
            GL.glVertex3fv(xij)
        GL.glEnd()
        GL.glPopName()

        
def draw_polygon_elems(x,e,n,c,alpha,objtype):
    """Draw a collection of polygon elements.

    This function is like draw_polygons, but the vertices of the polygons
    are specified by a (coords,elems) tuple.
    x : float (npts,3) : coordinates
    e : int32 (nel,nplex) : element connectivity
    n : float (nel,3) or (nel,nplex,3) normals.
    c : float (nel,3) or (nel,nplex,3) colors
    alpha : float
    objtype : GL Object type (-1 = auto)
    """
    draw_polygons(x[e],n,c,alpha,objtype)
    

def pick_polygon_elems(x,e,objtype):
    """Mimics draw_polygon_elems for picking purposes.

    x : float (npts,3) : coordinates
    e : int32 (nel,nplex) : element connectivity
    objtype : GL Object type (-1 = auto)
    """
    pick_polygons(x[e],objtype)
    
### End