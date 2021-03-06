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
"""Curves

Examples showing the use of the 'curve' plugin

"""
from __future__ import print_function
_status = 'checked'
_level = 'normal'
_topics = ['geometry','curve']
_techniques = ['widgets','persistence','import','spline']

from gui.draw import *

from plugins.curve import *
from plugins.nurbs import *
from odict import ODict


ctype_color = [ 'red','green','blue','cyan','magenta','yellow','white' ]
point_color = [ 'black','white' ]

open_or_closed = { True:'A closed', False:'An open' }

TA = None


curvetypes = [
    'PolyLine',
    'BezierSpline',
    'BezierSpline2',
    'NaturalSpline',
    'NurbsCurve',
]


def drawCurve(ctype,dset,closed,degree,endcond,curl,ndiv,ntot,extend,spread,approx,cutWP=False,scale=None,frenet=False,avgdir=True,upvector=None):
    global S,TA
    P = dataset[dset]
    text = "%s %s with %s points" % (open_or_closed[closed],ctype.lower(),len(P))
    if TA is not None:
        undecorate(TA)
    TA = drawText(text,10,20,font='sans',size=20)
    draw(P, color='black',nolight=True)
    drawNumbers(Formex(P))
    if ctype == 'PolyLine':
        S = PolyLine(P,closed=closed)
    elif ctype == 'BezierSpline':
        S = BezierSpline(P,degree=degree,curl=curl,closed=closed,endzerocurv=(endcond,endcond))
    elif ctype == 'BezierSpline2':
        S = BezierSpline(P,degree=2,closed=closed)
    elif ctype == 'NaturalSpline':
        S = NaturalSpline(P,closed=closed,endzerocurv=(endcond,endcond))
        directions = False
    elif ctype == 'NurbsCurve':
        S = NurbsCurve(P,closed=closed)#,blended=closed)
        scale = None
        directions = False
        drawtype = 'Curve'

    if scale:
        S = S.scale(scale)

    im = curvetypes.index(ctype)
    print("%s control points" % S.coords.shape[0])
    #draw(S.coords,color=red,nolight=True)

    if approx:
        if spread:
            PL = S.approx(ndiv=ndiv,ntot=ntot)
        else:
            PL = S.approx(ndiv=ndiv)

        if cutWP:
            PC = PL.cutWithPlane([0.,0.42,0.],[0.,1.,0.])
            draw(PC[0],color=red)
            draw(PC[1],color=green)
        else:
            draw(PL, color=ctype_color[im])
        draw(PL.pointsOn(),color=black)

    else:
        draw(S,color=ctype_color[im],nolight=True)


    ## if directions:
    ##     t = arange(2*S.nparts+1)*0.5
    ##     ipts = S.pointsAt(t)
    ##     draw(ipts)
    ##     idir = S.directionsAt(t)
    ##     drawVectors(ipts,0.2*idir)

    if frenet:
        if approx:
            C = PL
        else:
            C = S
        X,T,N,B = C.frenet(upvector=upvector,avgdir=avgdir)[:4]
        drawVectors(X,T,size=1.,nolight=True,color='red')
        drawVectors(X,N,size=1.,nolight=True,color='green')
        drawVectors(X,B,size=1.,nolight=True,color='blue')
        if  C.closed:
            X,T,N,B = C.frenet(upvector=upvector,avgdir=avgdir,compensate=True)[:4]
            drawVectors(X,T,size=1.,nolight=True,color='magenta')
            drawVectors(X,N,size=1.,nolight=True,color='yellow')
            drawVectors(X,B,size=1.,nolight=True,color='cyan')
        #print(T,N,B)



dataset = [
    Coords([[1., 0., 0.],[0., 1., 0.],[-1., 0., 0.],  [0., -1., 0.]]),
    Coords([[6., 7., 12.],[9., 5., 6.],[11., -2., 6.],  [9.,  -4., 14.]]),
    Coords([[-5., -10., -4.], [-3., -5., 2.],[-4., 0., -4.], [-4.,  5, 4.],
            [6., 3., -1.], [6., -9., -1.]]),
    Coords([[-1., 7., -14.], [-4., 7., -8.],[-7., 5., -14.],[-8., 2., -14.],
            [-7.,  0, -6.], [-5., -3., -11.], [-7., -4., -11.]]),
    Coords([[-1., 1., -4.], [1., 1., 2.],[2.6, 2., -4.], [2.9,  3.5, 4.],
            [2., 4., -1.],[1.,3., 1.], [0., 0., 0.], [0., -3., 0.],
            [2., -1.5, -2.], [1.5, -1.5, 2.], [0., -8., 0.], [-1., -8., -1.],
            [3., -3., 1.]]),
    Coords([[0., 1., 0.],[0., 0.1, 0.],[0.1, 0., 0.],  [1., 0., 0.]]),
    Coords([[0., 1., 0.],[0.,0.,0.],[0.,0.,0.],[1., 0., 0.]]),
    Coords([[0.,0.,0.],[1.,0.,0.],[1.,1.,1.],[0.,1.,0.]]).scale(3),
    ]

_items = [
    _I('DataSet','0',choices=map(str,range(len(dataset)))),
    _I('CurveType',choices=curvetypes),
    _I('Closed',False),
    _I('Degree',3,min=1,max=3),
    _I('Curl',1./3.),
    _I('EndCurvatureZero',False),
    _G('Approximation',[
        _I('Ndiv',4),
        _I('SpreadEvenly',False),
        _I('Ntot',40),
        ],checked=False),
    _I('ExtendAtStart',0.0),
    _I('ExtendAtEnd',0.0),
    _I('Scale',[1.0,1.0,1.0]),
    _I('Clear',True),
    _G('FrenetFrame',[
        _I('AvgDirections',True),
        _I('AutoUpVector',True),
        _I('UpVector',[0.,0.,1.]),
        ],checked=False),
    _I('CutWithPlane',False),
    ]

_enablers = [
    ('CurveType','BezierSpline','Degree','Curl','EndCurvatureZero'),
    ('SpreadEvenly',True,'Ntot'),
    ('AutoUpVector',False,'UpVector'),
    ]


clear()
setDrawOptions({'bbox':'auto','view':'front'})
linewidth(2)
flat()

dialog = None

import script


def close():
    global dialog
    if dialog:
        dialog.close()
        dialog = None
    # Release script lock
    scriptRelease(__file__)



def show(all=False):
    dialog.acceptData()
    res = dialog.results
    if res['AutoUpVector']:
        res['UpVector'] = None
    globals().update(res)
    export({'_Curves_data_':res})
    if Clear:
        clear()
    if all:
        Types = curvetypes
    else:
        Types = [CurveType]
    setDrawOptions({'bbox':'auto'})
    for Type in Types:
        drawCurve(Type,int(DataSet),Closed,Degree,EndCurvatureZero,Curl,Ndiv,Ntot,[ExtendAtStart,ExtendAtEnd],SpreadEvenly,Approximation,CutWithPlane,Scale,FrenetFrame,AvgDirections,UpVector)
        setDrawOptions({'bbox':None})

def showAll():
    show(all=True)

def timeOut():
    showAll()
    wait()
    close()


def run():
    global dialog
    dialog = Dialog(
        items=_items,
        enablers=_enablers,
        caption='Curve parameters',
        actions = [('Close',close),('Clear',clear),('Show All',showAll),('Show',show)],
        default='Show')

    if '_Curves_data_' in pf.PF:
        #print pf.PF['_Curves_data_']
        dialog.updateData(pf.PF['_Curves_data_'])

    dialog.timeout = timeOut
    dialog.show()
    # Block other scripts
    scriptLock(__file__)



if __name__ == 'draw':
    run()
# End
