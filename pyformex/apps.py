# $Id$
##
##  This file is part of pyFormex 0.8.6  (Mon Jan 16 21:15:46 CET 2012)
##  pyFormex is a tool for generating, manipulating and transforming 3D
##  geometrical models by sequences of mathematical operations.
##  Home page: http://pyformex.org
##  Project page:  http://savannah.nongnu.org/projects/pyformex/
##  Copyright 2004-2011 (C) Benedict Verhegghe (benedict.verhegghe@ugent.be) 
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
"""pyFormex apps initialization.

This module contains the functions to detect and load the pyFormex
applications.
"""

import pyformex as pf
import utils
import os,sys


class AppDir(object):
    """Application directory

    An AppDir is a directory containing pyFormex applications.
    When creatig an AppDir, its path is added to sys.path
    """
    known_dirs = {
        'examples': pf.cfg['examplesdir'],
        }

    def __init__(self,path,name=None,create=True):
        if not path:
            try:
                path = AppDir.known_dirs[name.lower()]
            except:
                raise ValueError,"Expected a path to initialize AppDir"

        self.path = checkAppdir(path)
        if self.path is None:
            raise ValueError,"Invalid application path %s" % path

        # Add the parent path to sys.path if it is not there
        parent = os.path.dirname(self.path)
        self.added = parent not in sys.path
        if self.added:
            sys.path.insert(1,parent)
        
        self.pkg = os.path.basename(self.path)
        if name is None:
            self.name = self.pkg.capitalize()
        else:
            self.name = name
        pf.debug("Created %s" % self,pf.DEBUG.CONFIG)

    def __repr__(self):
        return "AppDir %s at %s (%s)" % (self.name,self.path,self.pkg)


def setAppDirs():
    """Set the configured application directories"""
    # If this is a reset, first remove sys.path components
    try:
        for p in pf.appdirs:
            if p.added:
                parent = os.path.dirname(p.path)
                sys.path.remove(parent)
        print 'SYSPATH IS NOW:',sys.path
    except:
        pass

    pf.appdirs = [ AppDir(i[1],i[0]) for i in pf.cfg['appdirs'] ]
    for p in pf.appdirs:
        pf.debug(str(p),pf.DEBUG.CONFIG)


def addAppDir(d):
    """Add the application directory d to the sys.path

    d should be a valid path, chacked with checkAppdir
    """
    
    adddirs = [ a for a in adddirs if not a in sys.path ]
    #print "appdir parents to add",adddirs
    sys.path[1:1] = adddirs
    return appdirs


def checkAppdir(d):
    """Check that a directory d can be used as a pyFormex application path.

    If the path does not exist, it is created.
    If no __init__.py exists, it is created.
    If __init__.py exists, it is not checked.

    If successful, returns the path, else None
    """
    if not os.path.exists(d):
        try:
            os.makedirs(d)
        except:
            return None

    if not os.path.isdir(d):
        return None

    initfile = os.path.join(d,'__init__.py')
    if os.path.exists(initfile):
        return os.path.dirname(initfile)
        
    try:
        f = open(initfile,'w')
        f.write("""# $Id$
\"\"\"pyFormex application directory.

Do not remove this file. It is used by pyFormex to flag the parent
directory as a pyFormex application path. 
\"\"\"
# End
""")
        f.close()
        return os.path.dirname(initfile)
    except:
        return None


def load(appname,refresh=False):
    """Load the named app

    If refresh is True, the module will be reloaded if it was already loaded
    before.
    On succes, returns the loaded module
    """
    pf.debug("Loading %s" % appname,pf.DEBUG.APPS)
    try:
        __import__(appname)
        app = sys.modules[appname]
        if refresh:
            reload(app)
        return app
    except:
        if pf.cfg['raiseapploadexc']:
            raise
        else:
            return None


def findmodule(mod):
    """Find the path a module would be loaded from"""
    import sys, imp, os
    path = sys.path
    for i in mod.split('.'):
        path = [imp.find_module(i,path)[1],]
    path = path[0] if os.path.isdir(path[0]) else os.path.dirname(path[0])
    return path


def findAppSource(appname):
    """Find the source file of an application"""
    path = findmodule(appname)
    fn = os.path.join(path,appname.split('.')[-1]+'.py')
    return fn

    
def unload(appname):
    """Try to unload an application"""
    name = 'apps.'+appname
    if name in sys.modules:
        app = sys.modules[name]
        refcnt = sys.getrefcount(app)
        if refcnt == 4:
            pf.debug("Unloading %s" % name,pf.DEBUG.APPS)
            ## k = globals().keys()
            ## k.sort()
            ## print k
            del globals()[appname]
            del sys.modules[name]
            ## refcnt = sys.getrefcount(app)
            ## print refcnt
            del app
        else:
            print "Can not unload %s" % name
    else:
        print "Module %s is not loaded" % name


def listLoaded():
    loaded = [ m for m in sys.modules.keys() if m.startswith('apps.') ]
    loaded.sort()
    return loaded
    

def detect(appdir):
    # Detect, but do not load!!!!
    # because we are using this on import (before some applications can load)
    files = utils.listTree(appdir,listdirs=False,excludedirs=['.*'],includefiles=['.*\.py$'])
    apps = [ os.path.basename(f) for f in files ]
    apps = [ os.path.splitext(f)[0] for f in apps if f[0] not in '._' ]
    apps.sort()
        
    return apps
       

_available_apps = detect(os.path.dirname(__file__))


# End
