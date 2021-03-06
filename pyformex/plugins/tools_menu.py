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

"""tools_menu.py

Graphic Tools plugin menu for pyFormex.
"""
from __future__ import print_function

import pyformex as pf
from gui import menu

from geometry_menu import autoName
import utils
from formex import *
from gui.draw import *
from gui.widgets import simpleInputItem as _I
from plugins import objects
from plugins.tools import *
from plugins.trisurface import TriSurface



def editFormex(F,name):
    """Edit a Formex"""
    items = [('coords',repr(array(F.coords)),'text')]
    if F.prop is not None:
        items.append(('prop',repr(array(F.prop)),'text'))
    items.append(('eltype',F.eltype))
    res = askItems(items)
    if res:
        x = eval(res['coords'])
        p = res.get('eltype',None)
        if type(p) is str:
            p = eval(p)
        e = res['eltype']

        print(x)
        print(p)
        print(e)
        F.__init__(x,F.prop,e)

Formex.edit = editFormex


def command():
    """Execute an interactive command."""
    res = askItems([('command','','text')])
    if res:
        cmd = res['command']
        print("Command: %s" % cmd)
        exec(cmd)

##################### database tools ##########################

def _init_():
    global database,_drawables
    database = pf.GUI.database
    _drawables = pf.GUI.selection['geometry']


def printall():
    """Print all global variable names."""
    print(listAll(sort=True))


def printval():
    """Print selected global variables."""
    database.ask()
    database.printval()


def printbbox():
    """Print selected global variables."""
    database.ask()
    database.printbbox()


def keep_():
    """Forget global variables."""
    database.ask()
    database.keep()


def forget_():
    """Forget global variables."""
    database.ask()
    database.forget()


def create():
    """Create a new global variable with default initial contents."""
    res = askItems([('name','')])
    if res:
        name = res['name']
        if name in database:
            warning("The variable named '%s' already exists!")
        else:
            export({name:'__initial__'})


def edit():
    """Edit a global variable."""
    database.ask(mode='single')
    F = database.check(single=True)
    if F is not None:
        name = database.names[0]
        if hasattr(F,'edit'):
            # Call specialized editor
            F.edit(name)
        else:
            # Use general editor
            res = askItems([(name,repr(F),'text')])
            if res:
                print(res)
                pf.PF.update(res)


def rename_():
    """Rename a global variable."""
    database.ask(mode='single')
    F = database.check(single=True)
    if F is not None:
        oldname = database.names[0]
        res = askItems([('Name',oldname)],caption = 'Rename variable')
        if res:
            name = res['Name']
            export({name:F})
            database.forget()
            database.set(name)


def delete_all():
    printall()
    if ack("Are you sure you want to unrecoverably delete all global variables?"):
        forgetAll()




def dos2unix():
    fn = askFilename(multi=True)
    if fn:
        for f in fn:
            message("Converting file to UNIX: %s" % f)
            utils.dos2unix(f)


def unix2dos():
    fn = askFilename(multi=True)
    if fn:
        for f in fn:
            message("Converting file to DOS: %s" % f)
            utils.unix2dos(f)



##################### planes ##########################

planes = objects.DrawableObjects(clas=Plane)
pname = autoName(Plane)

def editPlane(plane,name):
    res = askItems([('Point',list(plane.point())),
                    ('Normal',list(plane.normal())),
                    ('Size',(list(plane.size()[0]),list(plane.size()[1])))],
                   caption = 'Edit Plane')
    if res:
        plane.P = res['Point']
        plane.n = res['Normal']
        plane.s = res['Size']

Plane.edit = editPlane


def createPlaneCoordsPointNormal():
    res = askItems([('Name',pname.next()),
                    ('Point',(0.,0.,0.)),
                    ('Normal',(1.,0.,0.)),
                    ('Size',((1.,1.),(1.,1.)))],
                   caption = 'Create a new Plane')
    if res:
        name = res['Name']
        p = res['Point']
        n = res['Normal']
        s = res['Size']
        P = Plane(p,n,s)
        export({name:P})
        draw(P)


def createPlaneCoords3Points():
    res = askItems([('Name',pname.next()),
                    ('Point 1',(0.,0.,0.)),
                    ('Point 2', (0., 1., 0.)),
                    ('Point 3', (0., 0., 1.)),
                    ('Size',((1.,1.),(1.,1.)))],
                   caption = 'Create a new Plane')
    if res:
        name = res['Name']
        p1 = res['Point 1']
        p2 = res['Point 2']
        p3 = res['Point 3']
        s = res['Size']
        pts=[p1, p2, p3]
        P = Plane(pts,size=s)
        export({name:P})
        draw(P)


def createPlaneVisual3Points():
    res = askItems([('Name',pname.next()),
                    ('Size',((1.,1.),(1.,1.)))],
                   caption = 'Create a new Plane')
    if res:
        name = res['Name']
        s = res['Size']
        picked = pick('point')
        pts = getCollection(picked)
        pts = asarray(pts).reshape(-1,3)
        if len(pts) == 3:
            P = Plane(pts,size=s)
            export({name:P})
            draw(P)
        else:
            warning("You have to pick exactly three points.")


################# Create Selection ###################

selection = None

def set_selection(obj_type):
    global selection
    selection = None
    selection = pick(obj_type)

def query(mode):
    set_selection(mode)
    print(report(selection))

def pick_actors():
    set_selection('actor')
def pick_elements():
    print(_drawables.names)
    set_selection('element')
def pick_points():
    set_selection('point')
def pick_edges():
    set_selection('edge')

def query_actors():
    query('actor')
def query_elements():
    query('element')
def query_points():
    query('point')
def query_edges():
    query('edge')

def query_distances():
    set_selection('point')
    print(reportDistances(selection))

def query_angle():
    showInfo("Select two line elements.")
    set_selection('element')
    print(reportAngles(selection))


def report_selection():
    if selection is None:
        warning("You need to pick something first.")
        return
    print(selection)
    print(report(selection))


def edit_point(pt):
    x,y,z = pt
    dia = None
    def close():
        dia.close()
    def accept():
        dia.acceptData()
        res = dia.results
        return [ res[i] for i in 'xyz' ]

    dia = widgets.InputDialog(
        items = [_I(x=x,y=y,z=z),]
        )
    dia.show()


def edit_points(K):
    if K.obj_type == 'point':
        for k in K.keys():
            o = pf.canvas.actors[k].object
            n =  _drawables.names[k]
            ind = K[k]
            print("CHANGING points %s of object %s" % (ind,n))
            print(o[ind])


def setpropCollection(K,prop):
    """Set the property of a collection.

    prop should be a single non-negative integer value or None.
    If None is given, the prop attribute will be removed from the objects
    in collection even the non-selected items.
    If a selected object does not have a setProp method, it is ignored.
    """
    if K.obj_type == 'actor':
        obj = [ pf.canvas.actors[i] for i in K.get(-1,[]) ]
        for o in obj:
            if hasattr(o,'setProp'):
                o.setProp(prop)

    elif K.obj_type in ['element','point']:
        for k in K.keys():
            a = pf.canvas.actors[k]
            o = a.object
            ## print "SETPROP ACTOR %s" % type(o)
            ## print _drawables
            ## n = _drawables.names[k]
            ## print "SETPROP DRAWABLE %s" % n
            ## O = named(n)
            ## print 'From actor: %s' % id(o)
            ## print 'From name: %s' % id(O)
            ## if id(o) != id(O):
            ##     raise RuntimeError,"The id of the drawn object does not match the selection"
            if prop is None:
                o.setProp(prop)
            elif hasattr(o,'setProp'):
                if not hasattr(o,'prop') or o.prop is None:
                    o.setProp(0)
                o.prop[K[k]] = prop
                o.setProp(o.prop)
                a.setColor(o.prop)
                a.redraw(mode=pf.canvas.rendermode)


def setprop_selection():
    """Set the property of the current selection.

    A property value is asked from the user and all items in the selection
    that have property have their value set to it.
    """
    if selection is None:
        warning("You need to pick something first.")
        return
    print(selection)
    res = askItems([['property',0]],
                   caption = 'Set Property Number for Selection (negative value to remove)')
    if res:
        prop = int(res['property'])
        if prop < 0:
            prop = None
        setpropCollection(selection,prop)
        removeHighlight()


def grow_selection():
    if selection is None:
        warning("You need to pick something first.")
        return
    print(selection)
    res = askItems([('mode','node','radio',['node','edge']),
                    ('nsteps',1),
                    ],
                   caption = 'Grow method',
                   )
    if res:
        growCollection(selection,**res)
    print(selection)
    highlightElements(selection)


def partition_selection():
    """Partition the current selection and show the result."""
    if selection is None:
        warning("You need to pick something first.")
        return
    if not selection.obj_type in ['actor','element']:
        warning("You need to pick actors or elements.")
        return
    for A in pf.canvas.actors:
        if not A.getType() == TriSurface:
            warning("Currently I can only partition TriSurfaces." )
            return
    partitionCollection(selection)
    highlightPartitions(selection)


def get_partition():
    """Select some partitions from the current selection and show the result."""
    if selection is None:
        warning("You need to pick something first.")
        return
    if not selection.obj_type in ['partition']:
        warning("You need to partition the selection first.")
        return
    res = askItems([['property',[1]]],
                 caption='Partition property')
    if res:
        prop = res['property']
        getPartition(selection,prop)
        highlightPartitions(selection)


def export_selection():
    if selection is None:
        warning("You need to pick something first.")
        return
    sel = getCollection(selection)
    if len(sel) == 0:
        warning("Nothing to export!")
        return
    options = ['List','Single items']
    default = options[0]
    if len(sel) == 1:
        default = options[1]
    res = askItems([
        _I('Export with name',''),
        _I('Export as',default,itemtype='radio',choices=options),
        ])
    if res:
        name = res['Export with name']
        opt = res['Export as'][0]
        if opt == 'L':
            export({name:sel})
        elif opt == 'S':
            export(dict([ (name+"-%s"%i,v) for i,v in enumerate(sel)]))


def sendMail():
    import sendmail
    sender = pf.cfg['mail/sender']
    if not sender:
        warning("You have to configure your email settings first")
        return

    res = askItems([
        _I('sender',sender,text="From:",readonly=True),
        _I('to','',text="To:"),
        _I('cc','',text="Cc:"),
        _I('subject','',text="Subject:"),
        _I('text','',itemtype='text',text="Message:"),
       ])
    if not res:
        return

    msg = sendmail.message(**res)
    print(msg)
    to = res['to'].split(',')
    cc = res['cc'].split(',')
    sendmail.sendmail(message=msg,sender=res['sender'],to=to+cc)
    print("Mail has been sent to %s" % to)
    if cc:
        print("  with copy to %s" % cc)

###################### images #############################

def selectImage(extra_items=[]):
    """Open a dialog to read an image file.

    """
    global image
    from gui.widgets import ImageView
    from plugins.imagearray import resizeImage

    # some default values
    filename = getcfg('datadir')+'/butterfly.png'
    w,h = 200,200
    image = None # the loaded image
    diag = None # the image dialog

    # construct the image previewer widget
    viewer = ImageView(filename,maxheight=h)

    def select_image(fn):
        """Helper function to load and preview image"""
        fn = askImageFile(fn)
        if fn:
            viewer.showImage(fn)
            load_image(fn)
        return fn

    def load_image(fn):
        """Helper function to load the image and set its size in the dialog"""
        global image
        image = resizeImage(fn)
        if image.isNull():
            warning("Could not load image '%s'" % fn)
            return None

        w,h = image.width(),image.height()
        print("size = %sx%s" % (w,h))

        diag = currentDialog()
        if diag:
            diag.updateData({'nx':w,'ny':h})

        maxsiz = 40000.
        if w*h > maxsiz:
            scale = sqrt(maxsiz/w/h)
            w = int(w*scale)
            h = int(h*scale)
        return w,h

    res = askItems([
        _I('filename',filename,text='Image file',itemtype='button',func=select_image),
        _I('viewer',viewer,itemtype='widget'),  # the image previewing widget
        _I('nx',w,text='width'),
        _I('ny',h,text='height'),
        ] + extra_items)

    if not res:
        return None

    if image is None:
        print("Loading image")
        load_image(filename)

    image = resizeImage(image,res['nx'],res['ny'])
    return image,res


def showImage():
    clear()
    im,res = selectImage()
    if im:
        drawImage(im)

def showImage3D():
    clear()
    im,res = selectImage([_I('pixel cell',choices=['dot','quad'])])
    if im:
        drawImage3D(im,pixel=res['pixel cell'])


################### menu #################

_menu = 'Tools'

def create_menu():
    """Create the Tools menu."""
    _init_()
    MenuData = [
        ('Global &Variables',[
            ('  &List All',printall),
            ('  &Select',database.ask),
            ('  &Print Value',printval),
            ('  &Print BBox',printbbox),
            ('  &Draw',_drawables.ask),
            ('  &Create',create),
            ('  &Change Value',edit),
            ('  &Rename',rename_),
            ('  &Keep',keep_),
            ('  &Delete',forget_),
            ('  &Delete All',delete_all),
            ]),
        ("---",None),
        ('&Execute pyFormex command',command),
        ("&DOS to Unix",dos2unix,dict(tooltip="Convert a text file from DOS to Unix line terminators")),
        ("&Unix to DOS",unix2dos),
        ("Send &Mail",sendMail),
        ("---",None),
        ("&Create Plane",[
            ("Coordinates",
                [("Point and normal", createPlaneCoordsPointNormal),
                ("Three points", createPlaneCoords3Points),
                ]),
            ("Visually",
                [("Three points", createPlaneVisual3Points),
                ]),
            ]),
        ("&Select Plane",planes.ask),
        ("&Draw Selection",planes.draw),
        ("&Forget Selection",planes.forget),
        ("---",None),
        ("Show an &Image file on the canvas",showImage),
        ("Show an &Image file as Formex",showImage3D),
        ("---",None),
        ('&Pick',[
            ("&Actors",pick_actors),
            ("&Elements",pick_elements),
            ("&Points",pick_points),
            ("&Edges",pick_edges),
            ]),
        ('&Edit Points',edit_points),
        ("&Remove Highlights",removeHighlight),
        ("---",None),
        ('&Selection',[
            ('&Create Report',report_selection),
            ('&Set Property',setprop_selection),
            ('&Grow',grow_selection),
            ('&Partition',partition_selection),
            ('&Get Partition',get_partition),
            ('&Export',export_selection),
            ]),
        ("---",None),
        ('&Query',[
            ('&Actors',query_actors),
            ('&Elements',query_elements),
            ('&Points',query_points),
            ('&Edges',query_edges),
            ('&Distances',query_distances),
            ('&Angle',query_angle),
            ]),
        ("---",None),
        ('&Reload',reload_menu),
        ("&Close",close_menu),
        ]
    return menu.Menu(_menu,items=MenuData,parent=pf.GUI.menu,before='help')


def show_menu():
    """Show the menu."""
    if not pf.GUI.menu.item(_menu):
        create_menu()


def close_menu():
    """Close the menu."""
    pf.GUI.menu.removeItem(_menu)


def reload_menu():
    """Reload the menu."""
    close_menu()
    show_menu()


####################################################################
######### What to do when the script is executed ###################

if __name__ == "draw":

    reload_menu()

# End
