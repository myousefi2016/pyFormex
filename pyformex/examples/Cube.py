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
"""Cube

Show (the faces of) a cube with different colors.
The user is presented a dialog where he can choose whether the faces
of the cube are drawn as triangles or as quadrilaterals, and what color
scheme is to be used: no color (black), a single color, a single color per
face, or a color gradient over the faces.
"""
from __future__ import print_function
_status = 'checked'
_level = 'normal'
_topics = ['geometry','surface']
_techniques = ['color','elements','reverse']

from gui.draw import *
from elements import Hex8

# This could be obtained from a Mesh conversion
def cube_tri(color=None):
    """Create a cube with triangles."""
    back = Formex('3:012934')
    left = back.rotate(-90,1)
    bot = back.rotate(90,0)
    front = back.translate(2,1)
    right = left.translate(0,1).reverse()
    top = bot.translate(1,1).reverse()
    back = back.reverse()
    faces = front+top+right+back+bot+left
    if color == 'None':
        color = 'white'
    elif color == 'Single':
        color = 'blue'
    elif color == 'Face':
        color = arange(1,7).repeat(2)
    elif color == 'Full':
        color = array([[4,5,7],[7,6,4],[7,3,2],[2,6,7],[7,5,1],[1,3,7],
                       [3,1,0],[0,2,3],[0,1,5],[5,4,0],[0,4,6],[6,2,0]])
    return faces,color


def cube_quad(color=None):
    """Create a cube with quadrilaterals."""
    v = Hex8.vertices
    f = Hex8.faces
    faces = Formex(v[f],eltype=f.eltype)
    if color == 'Single':
        color = 'red'
    elif color == 'Face':
        color = [4,1,5,2,6,3]
    elif color == 'Full':
        color = array([7,6,4,5,3,2,0,1])[f]
    return faces,color


def showCube(base,color):
    #print base,color
    if base == 'Triangle':
        cube = cube_tri
    else:
        cube = cube_quad
    cube,color = cube(color)
    clear()
    draw(cube,color=color)
    export({'cube':cube})
#    zoomAll()


def run():
    from gui import widgets

    clear()
    reset()
    smooth()
    view('iso')

    baseshape = ['Quad','Triangle']
    colormode = ['None','Single','Face','Full']

    while True:
        res = askItems([
            _I('All',False),
            _I('Base','Quad',choices=baseshape),
            _I('Color','Full',choices=colormode),
            ],caption="Make a selection or check 'All'")
        if not res:
            break;

        showall = res['All']
        if showall:
            bases = baseshape
            colors = colormode
        else:
            bases = [ res['Base'] ]
            colors = [ res['Color'] ]

        for base in bases:
            lights(False)

            for color in colors:
                showCube(base,color)
                if all:
                    sleep(1)

        # Break from endless loop if an input timeout is active !
        if widgets.input_timeout >= 0:
            break

if __name__ == 'draw':
    run()
# End
