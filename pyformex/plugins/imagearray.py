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
"""Convert bitmap images into numpy arrays.

This module contains functions to convert bitmap images into numpy
arrays and vice versa.

This code was based on ideas found on the PyQwt mailing list.
"""
from __future__ import print_function

import pyformex as pf
from gui import QtGui
QImage = QtGui.QImage
QColor = QtGui.QColor

import numpy as np
import utils


def resizeImage(image,w=0,h=0):
    """Load and optionally resize an image.

    Parameters:

    - `image`: a QImage, or any data that can be converted to a QImage,
      e.g. the name of a raster image file.
    - `w`, `h`: requested size in pixels of the image.
      A value <= 0 will be replaced with the corresponding actual size of
      the image.

    Returns a QImage with the requested size.
    """
    if not isinstance(image,QImage):
        image = QImage(image)

    W,H = image.width(),image.height()
    if w <= 0:
        w = W
    if h <= 0:
        h = H
    if w != W or h != H:
        image = image.scaled(w,h)

    return image


def image2numpy(image,resize=(0,0),order='RGBA',flip=True,indexed=None,expand=None):
    """Transform an image to a Numpy array.

    Parameters:

    - `image`: a QImage or any data that can be converted to a QImage,
      e.g. the name of an image file, in any of the formats supported by Qt.
      The image can be a full color image or an indexed type. Only 32bit
      and 8bit images are currently supported.
    - `resize`: a tuple of two integers (width,height). Positive value will
      force the image to be resized to this value.
    - `order`: string with a permutation of the characters 'RGBA', defining
      the order in which the colors are returned. Default is RGBA, so that
      result[...,0] gives the red component. Note however that QImage stores
      in ARGB order. You may also specify a subset of the 'RGBA' characters,
      in which case you will only get some of the color components. An often
      used value is 'RGB' to get the colors without the alpha value.
    - `flip`: boolean: if True, the image scanlines are flipped upside down.
      This is practical because image files are usually stored in top down
      order, while OpenGL uses an upwards positive direction, requiring a
      flip to show the image upright.
    - `indexed`: True, False or None.

      - If True, the result will be an indexed image where each pixel color
        is an index into a color table. Non-indexed image data will be
        converted.

      - If False, the result will be a full color array specifying the color
        of each pixel. Indexed images will be converted.

      - If None (default), no conversion is done and the resulting data are
        dependent on the image format. In all cases both a color and a
        colortable will be returned, but the latter will be None for
        non-indexed images.

    - `expand`: deprecated, retained for compatibility

    Returns:

    - if `indexed` is False: an int8 array with shape (height,width,4), holding
      the 4 components of the color of each pixel. Order of the components
      is as specified by the `order` argument. Indexed image formats will
      be expanded to a full color array.

    - if `indexed` is True: a tuple (colors,colortable) where colors is an
      (height,width) shaped int array of indices into the colortable,
      which is an int8 array with shape (ncolors,4).

    - if `indexed` is None (default), a tuple (colors,colortable) is returned,
      the type of which depend on the original image format:

      - for indexed formats, colors is an int (height,width) array of indices
        into the colortable, which is an int8 array with shape (ncolors,4).

      - for non-indexed formats, colors is a full (height,width,4) array
        and colortable is None.
    """
    if expand is not None:
        utils.warn("depr_image2numpy_arg")
        indexed = not expand


    image = resizeImage(image,*resize)

    if indexed:
        image = image.convertToFormat(QImage.Format_Indexed8)

    h,w = image.height(),image.width()

    if image.format() in (QImage.Format_ARGB32_Premultiplied,
                          QImage.Format_ARGB32,
                          QImage.Format_RGB32):
        buf = image.bits()
        if not pf.options.pyside:
            buf = buf.asstring(image.numBytes())
        ar = np.frombuffer(buf,dtype='ubyte',count=image.numBytes()).reshape(h,w,4)
        idx = [ 'BGRA'.index(c) for c in order ]
        ar = ar[...,idx]
        ct = None

    elif image.format() == QImage.Format_Indexed8:
        ct = np.array(image.colorTable(),dtype=np.uint32)
        #print("IMAGE FORMAT is INDEXED with %s colors" % ct.shape[0])
        ct = ct.view(np.uint8).reshape(-1,4)
        idx = [ 'BGRA'.index(c) for c in order ]
        ct = ct[...,idx]
        buf = image.bits()
        if not pf.options.pyside:
            buf = buf.asstring(image.numBytes())
        ar = np.frombuffer(buf,dtype=np.uint8)
        if ar.size != w*h:
            pf.warning("Size of image data (%s) does not match the reported dimensions: %s x %s = %s" % (ar.size,w,h,w*h))
            #ar = ar[:w*h]
        ar = ar.reshape(h,-1)
        #print "IMAGE SHAPE IS %s" % str(ar.shape)

    else:
        raise ValueError("image2numpy only supports 32bit and 8bit images")

    # Put upright as expected
    if flip:
        ar = np.flipud(ar)

    # Convert indexed to nonindexed if requested
    if indexed is False and ct is not None:
            ar = ct[ar]
            ct = None

    # Return only full colors if requested
    if indexed is False:
        return ar
    else:
        return ar,ct


def numpy2qimage(array):
        if np.ndim(array) == 2:
                return gray2qimage(array)
        elif np.ndim(array) == 3:
                return rgb2qimage(array)
        raise ValueError("can only convert 2D or 3D arrays")


def gray2qimage(gray):
        """Convert the 2D numpy array `gray` into a 8-bit QImage with a gray
        colormap.  The first dimension represents the vertical image axis."""
        if len(gray.shape) != 2:
                raise ValueError("gray2QImage can only convert 2D arrays")

        gray = np.require(gray, np.uint8, 'C')

        h, w = gray.shape

        result = QImage(gray.data, w, h, QImage.Format_Indexed8)
        result.ndarray = gray
        for i in range(256):
                result.setColor(i, QColor(i, i, i).rgb())
        return result


def rgb2qimage(rgb):
        """Convert the 3D numpy array `rgb` into a 32-bit QImage.  `rgb` must
        have three dimensions with the vertical, horizontal and RGB image axes."""
        if len(rgb.shape) != 3:
                raise ValueError("rgb2QImage expects the first (or last) dimension to contain exactly three (R,G,B) channels")
        if rgb.shape[2] != 3:
                raise ValueError("rgb2QImage can only convert 3D arrays")

        h, w, channels = rgb.shape

        # Qt expects 32bit BGRA data for color images:
        bgra = np.empty((h, w, 4), np.uint8, 'C')
        bgra[...,0] = rgb[...,2]
        bgra[...,1] = rgb[...,1]
        bgra[...,2] = rgb[...,0]
        bgra[...,3].fill(255)

        result = QImage(bgra.data, w, h, QImage.Format_RGB32)
        result.ndarray = bgra
        return result



def image2glcolor(image,resize=(0,0)):
    """Convert a bitmap image to corresponding OpenGL colors.

    Parameters:

    - `image`: a QImage or any data that can be converted to a QImage,
      e.g. the name of an image file, in any of the formats supported by Qt.
      The image can be a full color image or an indexed type. Only 32bit
      and 8bit images are currently supported.
    - `resize`: a tuple of two integers (width,height). Positive value will
      force the image to be resized to this value.

    Returns a (w,h,3) shaped array of float values in the range 0.0 to 1.0,
    containing the OpenGL colors corresponding to the image RGB colors.
    By default the image is flipped upside-down because the vertical
    OpenGL axis points upwards, while bitmap images are stored downwards.
    """
    c = image2numpy(image,resize=resize,order='RGB',flip=True,indexed=False)
    c = c.reshape(-1,3)
    c = c / 255.
    return c, None


# Import images using PIL

def imagefile2string(filename):
    import Image
    im = Image.open(filename)
    nx,ny = im.size[0],im.size[1]
    try:
        data = im.tostring("raw","RGBA",0,-1)
    except SystemError:
        data = im.tostring("raw","RGBX",0,-1)
    return nx,ny,data



# Import images using dicom
_dicom_spacing = None

if utils.checkModule('dicom'):

    def loadImage_dicom(filename):
        """Load a DICOM image into a numpy array.

        This function uses the python-dicom module to load a DICOM image
        into a numpy array. See also :func:`loadImage_gdcm` for an
        equivalent using python-gdcm.

        Parameters:

        - `file`: the name of a DICOM image file

        Returns a 3D array with the pixel data of all the images. The first
          axis is the `z` value, the last the `x`.

        As a side effect, this function sets the global variable `_dicom_spacing`
        to a (3,) array with the pixel/slice spacing factors, in order (x,y,z).
        """
        import dicom
        global _dicom_spacing
        _dicom_spacing = None
        dcm = dicom.read_file(filename)
        pix = dcm.pixel_array
        _dicom_spacing = np.array(dcm.PixelSpacing + [dcm.SliceThickness])
        return pix

    readDicom = loadImage_dicom


if utils.checkModule('gdcm'):


    def loadImage_gdcm(filename):
        """Load a DICOM image into a numpy array.

        This function uses the python-gdcm module to load a DICOM image
        into a numpy array. See also :func:`loadImage_dicom` for an
        equivalent using python-dicom.

        Parameters:

        - `file`: the name of a DICOM image file

        Returns a 3D array with the pixel data of all the images. The first
          axis is the `z` value, the last the `x`.

        As a side effect, this function sets the global variable `_dicom_spacing`
        to a (3,) array with the pixel/slice spacing factors, in order (x,y,z).
        """
        import gdcm

        def get_gdcm_to_numpy_typemap():
            """Returns the GDCM Pixel Format to numpy array type mapping."""
            _gdcm_np = {gdcm.PixelFormat.UINT8  :np.int8,
                        gdcm.PixelFormat.INT8   :np.uint8,
                        #gdcm.PixelFormat.UINT12 :np.uint12,
                        #gdcm.PixelFormat.INT12  :np.int12,
                        gdcm.PixelFormat.UINT16 :np.uint16,
                        gdcm.PixelFormat.INT16  :np.int16,
                        gdcm.PixelFormat.UINT32 :np.uint32,
                        gdcm.PixelFormat.INT32  :np.int32,
                        #gdcm.PixelFormat.FLOAT16:np.float16,
                        gdcm.PixelFormat.FLOAT32:np.float32,
                        gdcm.PixelFormat.FLOAT64:np.float64 }
            return _gdcm_np


        def get_numpy_array_type(gdcm_pixel_format):
            """Returns a numpy array typecode given a GDCM Pixel Format."""
            return get_gdcm_to_numpy_typemap()[gdcm_pixel_format]


        def gdcm_to_numpy(image):
            """Convert a GDCM image to a numpy array.

            """
            fmt = image.GetPixelFormat()

            if fmt.GetScalarType() not in get_gdcm_to_numpy_typemap().keys():
                raise ValueError,"Unsupported Pixel Format\n%s"%fmt

            shape = (image.GetDimension(0),image.GetDimension(1))
            if image.GetNumberOfDimensions() == 3:
              shape = shape + (image.GetDimension(2),)
            if fmt.GetSamplesPerPixel() != 1:
                raise ValueError,"Can not read images with multiple samples per pixel."

            dtype = get_numpy_array_type(fmt.GetScalarType())
            gdcm_array = image.GetBuffer()
            data = np.frombuffer(gdcm_array,dtype=dtype).reshape(shape)
            spacing = np.array(image.GetSpacing())
            return data,spacing


        global _dicom_spacing
        r = gdcm.ImageReader()
        r.SetFileName(filename)
        if not r.Read():
            raise ValueError,"Could not read image file '%s'" % filename
        pix,_dicom_spacing = gdcm_to_numpy(r.GetImage())
        return pix

    readDicom = loadImage_gdcm


def dicom2numpy(files):
    """Read a set of DICOM image files.

    Parameters:

    - `files`: a list of file names of dicom images of the same size,
      or a directory containing such images. In the latter case, all the
      DICOM images in the directory will be read.

    Returns a tuple of:

    - `pixar`: a 3D array with the pixel data of all the images. The first
      axis is the `z` value, the last the `x`.
    - `scale`: a (3,) array with the scaling factors, in order (x,y,z).
    """
    if type(files) is str:
        files = utils.listTree(fp,listdirs=False,includefiles="*.dcm")
    # read and stack the images
    print("Using %s to read DICOM files" % readDicom.__name__)

    pixar = np.dstack([ readDicom(f) for f in files ])
    scale = _dicom_spacing
    return pixar,scale


# End
