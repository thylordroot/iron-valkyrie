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

from .image import Image
from .atlas import Atlas

class Sprite:
    
    # Properties
    
    def x(self, new=None):
        if (not new is None):
            self._x = new;
        return self._x;
       
    def y(self, new=None):
        if (not new is None):
            self._y = new;
        return self._y;
    
    def pos(self, new=None):
        if (not new is None):
            self._x = new[0]
            self._y = new[1]
        return (self._x, self._y)
    
    def frame(self, new=None):
        if (not new is None):
            self._frame = new;
        return self._frame

    def enabled(self, new=None):
        if (not new is None):
            self._enabled = new
        return self._enabled
    
    # Constructors
    
    def __init__(self, atlas, enabled=False):
        if (isinstance(atlas, Atlas)):
            self._atlas = atlas
        elif (isinstance(atlas, Image)):
            self._atlas = Atlas(atlas, atlas.width(), atlas.height(), 1)
        else:
            raise Exception("Input must be atlas or image")
    
        self._enabled = enabled
        self._x = 0
        self._y = 0
        self._frame = 0
    
    # Rendering
    
    def advanceFrame(self):
        self._frame = (self._frame + 1) % self._atlas.count()
    
    def render(self, buffer):
        self._atlas.compose(buffer, self._frame, self._x, self._y) 