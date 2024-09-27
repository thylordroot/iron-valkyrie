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
        
    def composeEx(self, img, srcX, srcY, destX, destY, width, height):
        myChannels = self.channels()
        theirChannels = img.channels();
        
        clipped = Image._clip(srcX, srcY, img.width(), img.height(),
            width, height)
        srcX = clipped[0]
        srcY = clipped[1]
            
        clipped = Image._clip(destX, destY, self.width(), self.height(),
            clipped[2], clipped[3])
        destX = clipped[0]
        destY = clipped[1]
        width = clipped[2]
        height = clipped[3]
        
        if (width < 1 or height < 1):
            return
        
        if (theirChannels == 3):
            if (myChannels == 3):
                self.copyEx(img, srcX, srcY, destX, destY, width, height)
                return 
        
        
        # We cannot directly copy, alpha blend instead
        srcSlice = img.slice(srcX, srcY, width, height)
        destSlice = self.slice(destX, destY, width, height)
        
        if (srcSlice.hasAlpha()):
            alphaBuf = srcSlice._alpha.astype(float) / 255
            result = srcSlice._img * alphaBuf + destSlice._img * (1 - alphaBuf)
            
            result = Image(result.astype(numpy.uint8))
        else:
            result = srcSlice
            
        
            
        # Now copy buffer over
        self.copyEx(result, 0, 0, destX, destY, width, height)
    
    def _clip(x, y, srcWidth, srcHeight, destWidth, destHeight):
        if (x < 0):
            destWidth += x
            x = 0
        if (y < 0):
            destHeight += y
            y = 0
        
        if (destWidth > srcWidth):
            destWidth = srcWidth
        if (destHeight > srcHeight):
            destHeight = srcHeight
            
        return (x, y, destWidth, destHeight)
    
    def _copyEx(self, srcSlice, destSlice):
        # Copy the color data 
        srcSlice = img._img[srcY:(srcY+height), srcX:(srcX+width)]
        destSlice = self._img[destY:(destY+height), destX:(destX+width)]
        
        numpy.copyto(destSlice, srcSlice)
        
        # Copy alpha channel
        if (self.hasAlpha()):
            destSlice = self._alpha[destY:(destY+height), destX:(destX+width)]
            
            # If there is alpha data, copy it now
            if (img.hasAlpha()):
                srcSlice = img._alpha[srcY:(srcY+height), srcX:(srcX+width)]
                numpy.copyto(destSlice, srcSlice)
            # Else, fill with solid alpha
            else:
                destSlice.fill(0xFF)
                
    def copyEx(self, img, srcX, srcY, destX, destY, width, height):
        # Clip copied region
        clip = Image._clip(srcX, srcY, img.width(), img.height(),
            width, height)
    
        # Copy the color data 
        srcSlice = img._img[srcY:(srcY+height), srcX:(srcX+width)]
        destSlice = self._img[destY:(destY+height), destX:(destX+width)]
        
        numpy.copyto(destSlice, srcSlice)
        
        # Copy alpha channel
        if (self.hasAlpha()):
            destSlice = self._alpha[destY:(destY+height), destX:(destX+width)]
            
            # If there is alpha data, copy it now
            if (img.hasAlpha()):
                srcSlice = img._alpha[srcY:(srcY+height), srcX:(srcX+width)]
                numpy.copyto(destSlice, srcSlice)
            # Else, fill with solid alpha
            else:
                raise Exception("Got here ({hasAlpha})".format(hasAlpha=img.hasAlpha()))
                
                destSlice.fill(0xFF)
        
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