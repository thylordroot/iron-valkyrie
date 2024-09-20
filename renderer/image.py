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
        return numpy.size(self._img, 2)
        
    def dim(self):
        return [self.width(), self.height()]
       
    # Constructors
        
    def __init__(self, img):
        self._img = img
    
    def create(width, height):
        return Image(numpy.zeros((height, width, 3), numpy.uint8))
        
    # Image Routines - Copy
    
    def _composeRGBFromRGBA(self, img, srcX, srcY, destX, destY, width, height):
        pass
    
    def composeEx(self, img, srcX, srcY, destX, destY, width, height):
        myChannels = self.channels()
        theirChannels = img.channels();
        if (theirChannels == 3):
            if (myChannels == 3):
                self.copyEx(img, srcC, srcY, destX, destY, width, height)
                return 
        elif (theirChannels == 4):
            if (myChannels == 3):
                self._composeRGBFromRGBA(img, srcX, srcY, destX, destY, width, height)
                return
    
    
    def copyEx(self, img, srcX, srcY, destX, destY, width, height):
        if (img.channels() == self.channels()):
            srcSlice = img._img[srcY:(srcY+height), srcX:(srcX+width)]
            destSlice = self._img[destY:(destY+height), destX:(destX+width)]
            numpy.copyto(destSlice, srcSlice)
       
        
    def copy(self, img):
        self.copyEx(img, 0, 0, 0, 0, img.width(), img.height())
    
    # Image Routines: Geometry
    
    def fillRect(self, x, y, width, height, color):
        cv2.rectangle(self._img, (x, y), (x+width, y+height), color, -1)
            
    
    def drawLine(self, x0, y0, x1, y1, color):
        pass
    
    # I/O
    
    def load(path):
        return Image(cv2.imread(path))
        
    def save(self, path):
        cv2.imwrite(path, self._img)