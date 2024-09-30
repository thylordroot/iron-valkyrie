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

from renderer.atlas import Atlas
from renderer.sprite import Sprite

class Scout(Sprite):
    _atlas = Atlas.load("assets\png\part1\spaceship-back.png", 48, 16, 2)
    
    # Properties
    
    def dx(self):
        return self._dx
        
    def dy(self):
        return self._dy
        
    def velocity(self, new=None):
        if (not new is None):
            self._dx = new[0]
            self._dy = new[1]
        return (self._dx, self._dy)
    
    # Constructors
    
    def __init__(self):
        super.__init__(Scout._atlas, true)
        self._dx = 0;
        self._dy = 0
    
    # Rendering
    
    def renderAndUpdate(buffer):
        self.render(buffer)
        self._x += self._dx;
        self._y += self._dy;
        self.advanceFrame()
        