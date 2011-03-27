#!/usr/bin/env pyformex --gui
# $Id$

"""Nurbs

level = 'advanced'
topics = ['geometry', 'curve']
techniques = ['nurbs','border']

.. Description

Nurbs
=====
"""

import simple
from plugins.curve import *
from plugins.nurbs import *


def uniformParamValues(self,n):
    """Create a set of uniform parameter values for the NurbsCurve"""
    umin = self.knots[0]
    umax = self.knots[-1]
    u = umin + arange(n+1) * (umax-umin) / n
    

def expandNurbsCurve():
    def derivatives(self,at,d=1):
        """Returns the points and derivatives up to d at parameter values at"""
        if type(at) is int:
            u = self.uniformKnotValues(at)
        else:
            u = at
            
        # sanitize arguments for library call
        ctrl = self.coords.astype(double)
        knots = self.knots.astype(double)
        u = asarray(u).astype(double)
        d = int(d)
        
        try:
            pts = nurbs.curveDerivs(ctrl,knots,u,d)
            if isnan(pts).any():
                print "We got a NaN"
                print pts
                raise RuntimeError
        except:
            raise RuntimeError,"Some error occurred during the evaluation of the Nurbs curve"

        # When using Coords4 normalized points, the derivatives all have w=0
        # (the points represent directions). We just strip off the w=0.
        return Coords(pts[...,:3])

    NurbsCurve.uniformParamValues = uniformParamValues
    NurbsCurve.derivatives = derivatives


expandNurbsCurve()                         
clear()
linewidth(2)
flat()

#    3*0    -     2*1     -    3*2    : 8 = 5+3
#    nctrl = nparts * degree + 1 
#    nknots = nctrl + degree + 1
#    nknots = (nparts+1) * degree + 2
#
# degree  nparts  nctrl   nknots
#    2      1       3        6
#    2      2       5        8
#    2      3       7       10
#    2      4       9       12
#    3      1       4        8
#    3      2       7       11
#    3      3      10       14
#    3      4      13       17
#    4      1       5       10 
#    4      2       9       14
#    4      3      13       18
#    5      1       6       12
#    5      2      11       17
#    5      3      16       22
#    6      1       7       14       
#    6      2      13       20
#    7      1       8       16
#    8      1       9       18

# This should be a valid combination of ntrl/degree
# drawing is only done if degree <= 7



def drawThePoints(N,n,color=None):
    umin = N.knots[N.degree]
    umax = N.knots[-N.degree-1]
    #print "Umin = %s, Umax = %s" % (umin,umax)
    u = umin + arange(n+1) * (umax-umin) / float(n)
    P = N.pointsAt(u)    
    draw(P,color=color,marksize=5)
    drawNumbers(P,color=color)
    
    XD = N.derivatives(u,5)[:3]
    if XD.shape[-1] == 4:
        XD = XD.toCoords()
    x,d,dd = XD[:3]
    #print "Point %s: Dir %s" % (x,d)
    x1 = x+0.1*d
    x2 = x+0.01*dd
    draw(x,marksize=10,color=yellow)
    draw(connect([Formex(x),Formex(x1)]),color=yellow,linewidth=3)
    #draw(connect([Formex(x),Formex(x2)]),color=cyan,linewidth=3)


def drawNurbs(control,degree,closed,blended,weighted=False,Clear=False):
    if Clear:
        clear()

    C = Formex(pattern(control)).toCurve()
    X = C.coords
    draw(C)
    draw(X,marksize=10)
    drawNumbers(X,leader='P',trl=[0.02,0.02,0.])
    if closed:
        # remove last point if it coincides with first
        x,e = Coords.concatenate([X[0],X[-1]]).fuse()
        if x.shape[0] == 1:
            X = X[:-1]
        blended=True
    draw(PolyLine(X,closed=closed),bbox='auto',view='front')
    if not blended:
        nX = ((len(X)-1) // degree) * degree + 1
        X = X[:nX]
    if weighted:
        wts = array([1.]*len(X))
        wts[1::2] = 0.5
        #print wts,wts.shape
    else:
        wts=None
    N = NurbsCurve(X,wts=wts,degree=degree,closed=closed,blended=blended)
    draw(N,color=red)
    drawThePoints(N,20,color=black)


clear()
setDrawOptions({'bbox':None})
linewidth(2)
flat()

dialog = None


def close():
    global dialog
    if dialog:
        dialog.close()
        dialog = None


def show():
    dialog.acceptData()
    res = dialog.results
    export({'_Nurbs_data_':res})
    drawNurbs(**res)


def timeOut():
    showAll()
    close()


predefined = [
    '51414336',
    '2584',
    '25984',
    '184',
    '514',
    '1234',
    '5858585858',
    '12345678',
    '121873',
    '1218973',
    '8585',
    '85985',
    '214121',
    '214412',
    '151783',
    ]
    
data_items = [
    _I('control',text='Control Points',choices=predefined),
    _I('degree',2),
    _I('closed',False),
    _I('blended',True,enabled=False),
    _I('weighted',False),
    _I('Clear',True),
    ]
input_enablers = [
    ('closed',False,'blended'),
    ]
  
dialog = Dialog(
    data_items,
    enablers = input_enablers,
    caption = 'Nurbs parameters',
    actions = [('Close',close),('Clear',clear),('Show',show)],
    default = 'Show',
    )

if pf.PF.has_key('_Nurbs_data_'):
    dialog.updateData(pf.PF['_Nurbs_data_'])

dialog.timeout = timeOut
dialog.show()
       

# End