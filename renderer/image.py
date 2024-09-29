#  Iron Valkyrie - A Demo Presentation
#
#    Copyright (C) 2024  thylordroot
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import cv2
import numpy
from .rect import Rect

class Image:
    # Properties

    def width(self):
        return numpy.size(self._img, 1)
        
    def height(self):
        return numpy.size(self._img, 0)
        
    def channels(self): 
        ret = numpy.size(self._img, 2)
        if (not self._alpha is None):
            ret = ret + 1
        return ret
        
    def hasAlpha(self):
        return not self._alpha is None
        
    def dim(self):
        return [self.width(), self.height()]
       
    def rect(self):
        return Rect(0, 0, self.width(), self.height())
       
    # Constructors
        
    def __init__(self, img, alpha = None):    
        # Strip out the alpha channel
        if (numpy.size(img, 2) == 4):
            if (alpha is None):
                alpha = img[:,:,3:4]
            img = img[:,:,0:3]
        # There is no alpha channel
        
        self._img = img
        self._alpha = alpha
    
    def create(width, height, channels=3):
        return Image(numpy.zeros((height, width, channels), numpy.uint8))
    
    # Image Routines - Linear Algebra
    def scale(self, fx, fy):
        return Image(cv2.resize(self._img, (0,0), fx=fx, fy=fy))
    
    # Image Routines - Copy
    
    def slice(self, x, y, width, height):
        yMax = y+height;
        xMax = x + width;
        ret = self._img[y:yMax, x:xMax]
        
        if (self.hasAlpha()):
            alpha = self._alpha[y:yMax, x:xMax]
        else:
            alpha = None
        return Image(ret, alpha)
        
    def sliceRect(self, rect):
        return self.slice(rect.x, rect.y, rect.width, rect.height)
        
    def _composeEx(self, img, src, dest):
    
        if (src.isDegenerate() or dest.isDegenerate()):
            return;
        
        myChannels = self.channels()
        theirChannels = img.channels();    
            
        # 
        if (theirChannels == 3):
            if (myChannels == 3):
                self._copyEx(img, src, dest)
                return 
        
        
        # We cannot directly copy, alpha blend instead
        srcSlice = img.sliceRect(src)
        destSlice = self.sliceRect(dest)
        
        if (srcSlice.hasAlpha()):
            alphaBuf = srcSlice._alpha.astype(float) / 255
            result = srcSlice._img * alphaBuf + destSlice._img * (1 - alphaBuf)
            
            result = Image(result.astype(numpy.uint8))
        else:
            result = srcSlice
            
        # Now copy buffer over
        self._copyEx(result, Rect(0, 0, src.width, src.height), dest) 
    
        pass
        
    def composeEx(self, img, srcX, srcY, destX, destY, width, height):
        # Clip source and destination
        clip = self._clip2(img, srcX, srcY, destX, destY, width, height)
        return self._composeEx(img, clip[0], clip[1])
        
    def _clip2(self, src, srcX, srcY, destX, destY, width, height):
        dest = self.rect();   
        
        # Make sure we have a rectangle
        if (isinstance(src, Image)):
            src = src.rect()
            
        return src.clip2(dest, srcX, srcY, destX, destY, width, height)
        
    def _copyEx(self, img, src, dest):
        if (src.isDegenerate() or dest.isDegenerate()):
            return;
        elif ((src.width != dest.width) or (src.height != dest.height)):
            raise Exception("Invalid Geometry");
           
        # Copy the color data 

        srcSlice = img._img[(src.y):(src.yBound()), (src.x):(src.xBound())]
        destSlice = self._img[(dest.y):(dest.yBound()), (dest.x):(dest.xBound())]
        
        # Copy BGR buffer
        numpy.copyto(destSlice, srcSlice)
        
        # Copy alpha channel
        if (self.hasAlpha()):
            #print("Handling alpha channel");
            destSlice = self._alpha[(dest.y):(dest.yBound()), (dest.x):(dest.xBound())]
            
            # If there is alpha data, copy it now
            if (img.hasAlpha()):
                srcSlice = img._alpha[(src.y):(src.yBound()), (src.x):(src.xBound())]
                numpy.copyto(destSlice, srcSlice)
            # Else, fill with solid alpha
            else:
                destSlice.fill(0xFF)
                
    def copyEx(self, img, srcX, srcY, destX, destY, width, height):
        # Clip source and destination
        clip = self._clip2(img, srcX, srcY, destX, destY, width, height)
        self._copyEx(img, clip[0], clip[1])
        
    def copy(self, img):
        self.copyEx(img, 0, 0, 0, 0, img.width(), img.height())
    
    def clone(self):
        img = numpy.copy(self._img)
        if (not self._alpha is None):
            alpha = numpy.copy(self._alpha)
        else:
            alpha = None
        return Image(img, alpha)
    
    # Image Routines: Replace
    
    def _replaceSingle(self, src, dest):
        mask = (self._img[:,:,0] == src[0]) & (self._img[:,:,1] == src[1]) & (self._img[:,:,2] == src[2])
        self._img[:,:,0:3][mask] = dest
        
    def _replaceList(self, src, dest):
        for i in range(0, len(src)):
            self._replaceSingle(src[i], dest[i])
    
    def replace(self, src, dest = None):
        if (isinstance(src, tuple) and isinstance(dest, tuple)):
            self._replaceSingle(src, dest)
        elif (isinstance(src, list) and isinstance(dest, list)):
            self._replaceList(src, dest)
        else:
            raise Exception("Don't know how to do replacement (src={src}, dest={dest}.",
                src=src, dest=dest)
    
    # Image Routines: Geometry
    
    def fillRect(self, x, y, width, height, color):
        cv2.rectangle(self._img, (x, y), (x+width, y+height), color, -1)
            
    def drawLine(self, x0, y0, x1, y1, color):
        pass
    
    # I/O
    
    def load(path):
        buffer = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        return Image(buffer)
        
    def save(self, path):
        # No alpha channel, do not write
        if (self._alpha is None):
            src = self._img
        # Merge the alpha channel
        else:
            src = numpy.zeros((self.height(), self.width(), 4), numpy.uint8)
            bgr = src[:,:,0:3]
            alpha = src[:,:,3:4]
            numpy.copyto(bgr, self._img)
        cv2.imwrite(path, src)
        
    # Conversion
    
    def __str__(self):
        return "[{width}x{height} image]".format(width=self.width(), height=self.height());