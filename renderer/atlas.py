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
#    but WITHOUT ANY WARRANTY; without even t implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .image import Image

class Atlas:
    # Properties
    
    def width(self):
        return self._width
        
    def height(self):
        return self._height
        
    def dim(self):
        return (self._width, self_height)
        
    def count(self):
        return self._count
        
    def pitch(self):
        return self._pitch
        
	# Constructors
    
    def __init__(self, src, width, height, count=-1):
        self._img = src
        self._width = width
        self._height = height
        self._pitch = (int(src.width()/width), int(src.height()/height))    
        if (count < 0): 
            count = self._pitch[0] * self._pitch[1]
        self._count = count;
        
    def load(path, width, height, count=-1):
        return Atlas(Image.load(path), width, height, count)