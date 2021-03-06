.. $Id$  -*- rst -*-
  
..
  This file is part of the pyFormex project.
  pyFormex is a tool for generating, manipulating and transforming 3D
  geometrical models by sequences of mathematical operations.
  Home page: http://pyformex.org
  Project page:  https://savannah.nongnu.org/projects/pyformex/
  Copyright (C) Benedict Verhegghe (benedict.verhegghe@ugent.be)
  Distributed under the GNU General Public License version 3 or later.
  
  
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see http://www.gnu.org/licenses/.
  
  

.. include:: <isonum.txt>
.. include:: defines.inc
.. include:: links.inc

.. _`development`: http://savannah.nongnu.org/projects/pyformex/

.. title:: pyFormex Home

.. meta::
   :description: pyFormex - A tool for generating, manipulating and operating on large geometrical models of 3D structures by sequences of mathematical transformations
   :keywords: Pyformex, 3D modeling, Geometry, Surface, Mesh, STL ,Finite Elements, Stent, Python, Numpy

.. toctree::
   :titlesonly:
   :hidden:

   documentation <http://www.nongnu.org/pyformex/doc/index.html>
   gallery
   support
   links

.. index:: About

About
=====
pyFormex is a program for generating, transforming and manipulating large
geometrical models of 3D structures by sequences of mathematical 
operations. Thanks to a powerful (Python based) scripting language,
pyFormex is very well suited for the automated design of spatial frame
structures. It provides a wide range of operations on surface meshes, 
like STL type triangulated surfaces. There are provisions to import medical 
scan images. pyFormex can also be used as a pre- and post-processor for 
Finite Element analysis programs. Finally, it might be used just for 
creating some nice graphics.

Using pyFormex, the topology of the elements and the final geometrical form
can be decoupled. Often, topology is created first and then mapped onto the
geometry. Through the scripting language, the user can define any sequence
of transformations, built from provided or user defined functions. 
This way, building parametric models becomes a natural thing.

While pyFormex is still under `development`_, it already provides a
fairly stable scripting language and an OpenGL GUI environment for
displaying and manipulating the generated structures.

.. index:: News
  
`News`_
=======

.. include:: news.inc

.. index::
   Documentation
   Project page
   

Overview
========

.. raw:: html

  <table class="contentstable" align="center" style="margin-left: 30px"><tr>
    <td width="50%">

      <p class="biglink"><a class="biglink" href="gallery.html">Gallery</a><br/><span class="linkdescr">to wet your appetite</span></p>

      <p class="biglink"><a class="biglink" href="contents.html">Contents</a><br/><span class="linkdescr">for a complete overview</span></p>

      <p class="biglink"><a class="biglink" href="http://savannah.nongnu.org/projects/pyformex/">Project page</a><br/><span class="linkdescr">where the development takes place</span></p>

      <p class="biglink"><a class="biglink" href="links.html">Links</a><br/><span class="linkdescr">to providers, users and just friends</span></p>

    </td><td width="50%">

      <p class="biglink"><a class="biglink" href="doc/index.html">Documentation</a><br/><span class="linkdescr">learn all about pyFormex</span></p>

      <p class="biglink"><a class="biglink" href="doc/install.html">Install</a><br/><span class="linkdescr">discover the many ways to install</span></p>

      <p class="biglink"><a class="biglink" href="support.html">Support</a><br/><span class="linkdescr">everyone at times needs help with something</span></p>

    </td></tr>
  </table>


.. index:: License

License 
======= 
This program is free software; you can redistribute it
and/or modify it under the terms of the `GNU General Public License`_
as published by the Free Software Foundation; either version 3 of the
License, or (at your option) any later version.
 


.. End
