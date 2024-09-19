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
        return numpy.size(self._img, 0)
        
    def height(self):
        return numpy.size(self._img, 1)
        
    def dim(self):
        return [self.width(), self.height()]
       
    # Constructors
        
    def __init__(self, img):
        self._img = img
    
    def create(width, height):
        return Image(numpy.zeros((width, height, 3), numpy.uint8))
        
    # Image Routines
    
    def composeEx(self, img, srcX, srcY, destX, destY, width, height):
        pass
        
    # I/O
    
    def load(path):
        return Frame(cv2.imread(path))
        
    def save(self, path):
        cv2.imwrite(path, self._img)