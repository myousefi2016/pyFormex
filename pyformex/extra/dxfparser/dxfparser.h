/* $Id$ */
//
//  This file is part of pyFormex 0.8.8  (Sun Nov  4 15:24:17 CET 2012)
//  pyFormex is a tool for generating, manipulating and transforming 3D
//  geometrical models by sequences of mathematical operations.
//  Home page: http://pyformex.org
//  Project page:  http://savannah.nongnu.org/projects/pyformex/
//  Copyright 2004-2011 (C) Benedict Verhegghe (benedict.verhegghe@ugent.be) 
//  Distributed under the GNU General Public License version 3 or later.
//
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see http://www.gnu.org/licenses/.
//


/**************************************************************************
  dxfparser.cc      DXF parser
 
  dxfparser uses the dxflib from QCAD to parse an AutoCAD .DXF file,
  and exports it as a script with function calling syntax. 
 
***************************************************************************/

#ifndef DXFPARSER_H
#define DXFPARSER_H

#include <dl_creationadapter.h>
#include <dl_dxf.h>


class MyDxfFilter : public DL_CreationAdapter {

  virtual void addArc(const DL_ArcData& d);
  virtual void addCircle(const DL_CircleData& d);
  virtual void addLine(const DL_LineData& d);
  virtual void addPolyline(const DL_PolylineData& d);
  virtual void addVertex(const DL_VertexData& d);

};

#endif // DXFPARSER_H
