# -*- coding: utf-8 -*-
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
"""Display help

"""
from __future__ import print_function

import pyformex as pf

import os,sys
import draw
import utils
import tempfile
import random
import viewport
from gettext import gettext as _


def help(page=None):
    """Display a html help page.

    If no page is specified, the help manual is displayed.

    If page is a string starting with 'http:', the page is displayed with
    the command set in pf.cfg['browser'], else with the command in
    pf.cfg['viewer']
    """
    if not page:
        page = pf.cfg['help/manual']
    if page.startswith('http:') or page.startswith('file:'):
        browser = pf.cfg['browser']
    else:
        browser = pf.cfg['viewer']
    pid = utils.spawn(' '.join([browser,page]))


def catchAndDisplay(expression):
    """Catch stdout from a Python expression and display it in a window."""
    save = sys.stdout
    try:
        f = tempfile.TemporaryFile('w+')
        sys.stdout = f
        eval(expression)
        f.seek(0)
        draw.showText(f.read())
    finally:
        sys.stdout = save


## def qappargs():
##     """Display informeation on the Qt application arguments."""
##     qtversion = utils.hasModule('pyqt4')
##     qtversion = '.'.join(qtversion.split('.')[:2])
##     link = "http://doc.trolltech.com/%s/qapplication.html#QApplication" % qtversion
##     help(link)

def opengl():
    """Display the OpenGL format description."""
    draw.showText(viewport.OpenGLFormat())

def detected():
    """Display the detected software components."""
    utils.checkAllModules()
    utils.checkExternal()
    draw.showText(utils.reportDetected())

def about():
    """Display short information about pyFormex."""
    draw.showInfo("""..

%s
%s

A tool for generating, manipulating and transforming 3D geometrical models by sequences of mathematical operations.

%s

Distributed under the GNU GPL version 3 or later
""" % (pf.Version,'='*len(pf.Version),pf.Copyright))

# List of developers/contributors (current and past)
_developers = [
    'Matthieu De Beule',
    'Gianluca De Santis',
    'Bart Desloovere',
    'Francesco Iannaccone',
    'Peter Mortier',
    'Tim Neels',
    'Tomas Praet',
    'Sofie Van Cauter',
    'Benedict Verhegghe',
    'Zhou Wenxuan',
    ]
random.shuffle(_developers)

def developers():
    """Display the list of developers."""
    random.shuffle(_developers)
    draw.showInfo("""
The following people have
contributed to pyFormex.
They are listed in random order.

%s

If you feel that your name was left
out in error, please write to
benedict.verhegghe@ugent.be.
""" % '\n'.join(_developers))


_cookies = [
    "Smoking may be hazardous to your health.",
    "Windows is a virus.",
    "Coincidence does not exist. Perfection does.",
    "It's all in the code.",
    "Python is the universal glue.",
    "Intellectual property is a mental illness.",
    "Programmers are tools for converting caffeine into code.",
    "There are 10 types of people in the world: those who understand binary, and those who don't.",
    "Linux: the choice of a GNU generation",
    "Everything should be made as simple as possible, but not simpler. (A. Einstein)",
    "Perfection [in design] is achieved, not when there is nothing more to add, but when there is nothing left to take away. (Antoine de Saint-Exupéry)",
    "Programming today is a race between software engineers striving to build bigger and better idiot-proof programs, and the universe trying to build bigger and better idiots. So far, the universe is winning. (Rick Cook)",
    "In theory, theory and practice are the same. In practice, they're not. (Yoggi Berra)",
    "Most good programmers do programming not because they expect to get paid or get adulation by the public, but because it is fun to program. (Linus Torvalds)",
    "Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live. (Martin Golding)",
    "If Microsoft had developed Internet, we could not ever see the source code of web pages. HTML might be a complied language then.",
    "What one programmer can do in one month, two programmers can do in two months.",
    "Windows 9x: n. 32 bit extensions and a graphical shell for a 16 bit patch to an 8 bit operating system originally coded for a 4 bit microprocessor, written by a 2 bit company that can't stand 1 bit of competition. (Cygwin FAQ)",
    "You know, when you have a program that does something really cool, and you wrote it from scratch, and it took a significant part of your life, you grow fond of it. When it's finished, it feels like some kind of amorphous sculpture that you've created. It has an abstract shape in your head that's completely independent of its actual purpose. Elegant, simple, beautiful.\nThen, only a year later, after making dozens of pragmatic alterations to suit the people who use it, not only has your Venus-de-Milo lost both arms, she also has a giraffe's head sticking out of her chest and a cherubic penis that squirts colored water into a plastic bucket. The romance has become so painful that each day you struggle with an overwhelming urge to smash the fucking thing to pieces with a hammer. (Nick Foster)",
    "One of my most productive days was throwing away 1000 lines of code. (Ken Thompson)",
    ]
random.shuffle(_cookies)

def roll(l):
    l.append(l.pop(0))

def cookie():
    draw.showInfo(_cookies[0],["OK"])
    roll(_cookies)


def showURL(link):
    """Show a html document in the browser.

    `link` is an URL of a html document. If it does not start with `http://`, this will
    be prepended. The resulting URL is passed to the user's default or configured browser.
    """
    if not link.startswith('http://'):
        link = 'http://'+link
    help(link)


def showFileOrURL(link):
    """Show a html document or a text file.

    `link` is either a file name or an URL of a html document.
    If `link` starts with `http://`, it is interpreted as an URL and the
    corresponding document is shown in the user's browser.
    Else, `link` is interpreted as a filename and if the file exists, it
    is shown in a pyFormex text window.
    """
    if link.startswith('http://'):
        showURL(link)
    else:
        draw.showFile(link,mono=not link.endswith('.rst'))


def searchText():
    from widgets import simpleInputItem as _I
    res = draw.askItems([
        _I('pattern','',text='String to grep'),
        _I('options','',text='Options',tooltip="Some cool options: -a (extended search), -i (ignore case), -f (literal string), -e (extended regexp)"),
        ])

    if res:
        out = utils.grepSource(relative=False,quiet=True,**res)
        draw.showText(out,mono=True,modal=False)



def createMenuData():
    """Returns the help menu data"""
    DocsMenuData = [(k,help,{'data':v}) for k,v in pf.cfg['help/docs']]
    Docs2MenuData = [(k,draw.showFile,{'data':v}) for k,v in pf.cfg['help/docs2']]
    LinksMenuData = [(k,showURL,{'data':v}) for k,v in pf.cfg['help/links']]

    try:
        MenuData = DocsMenuData + [
            (_('&Search text in source'),searchText),
            (_('&Current Application'),draw.showDoc),
            ('---',None),
            ] + Docs2MenuData + [
            (_('&Detected Software'),detected),
            (_('&OpenGL Format'),opengl),
            (_('&Fortune Cookie'),cookie),
            (_('&Favourite Links'),LinksMenuData),
            (_('&People'),developers),
            (_('&About'),about),
            ]
    except:
        MenuData = []

    if pf.installtype in 'SG':
        pyformexdir = pf.cfg['pyformexdir']
        devtodo = os.path.join(pyformexdir,"..","TODO")
        devhowto = os.path.join(pyformexdir,"..","HOWTO-dev.rst")
        devapp = os.path.join(pyformexdir,"..","scripts-apps.rst")
        devextra = os.path.join(pyformexdir,"..","install-extra.rst")
        #print pf.refcfg.help['developer']
        developer = [
            ('Developer HOWTO',devhowto),
            ('Scripts versus Apps',devapp),
            ('pyFormex TODO list',devtodo),
            ('Installation of extra software',devextra),
           ('Numpy documentation guidelines','http://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt'),
            ('re-structured text (reST)','http://docutils.sourceforge.net/rst.html')
            ]


        DevLinksMenuData = [(k,showFileOrURL,{'data':v}) for k,v in developer]
        MenuData += [
            ('---',None),
            (_('&Developer Guidelines'),DevLinksMenuData),
            ]

        def install_external(pkgdir,prgname):
            extdir = os.path.join(pf.cfg['pyformexdir'],'extra',pkgdir)
            sta,out = utils.runCommand("cd %s; make && gksu make install" % extdir)
            if sta:
                info = out
            else:
                if utils.hasExternal(prgname,force=True):
                    info = "Succesfully installed %s" % pkgdir
                else:
                    info ="You should now restart pyFormex!"
            draw.showInfo(info)
            return sta

        def install_dxfparser():
            install_external('dxfparser','pyformex-dxfparser')

        def install_postabq():
            install_external('postabq','pyformex-postabq')

        def install_gts():
            install_external('gts','gtsinside')


        MenuData.append((_('&Install Externals'),[
            (_('dxfparser'),install_dxfparser,{'tooltip':"Install dxfparser: requires libdxflib-dev!"}),
            (_('postabq'),install_postabq),
            (_('gts'),install_gts),
            ]))


        # DEV: Leave the following commented code as an example

        ## #
        ## # Test of the exit function
        ## #

        ## def testExit():
        ##     import guimain
        ##     ret = guimain.exitDialog()
        ##     print "ExitDialog returned: %s" % ret

        ## MenuData.append((_('&Test Functions'),[
        ##     (_('test exit'),testExit),
        ##     ]))


    return MenuData


# End
