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

from .font import Font
from .scene import Scene

class TextScroller(Scene):
    # Properties
    
    def font(self):
        return self._font;

    def anchor(self):
        return self._anchor

    def dim(self):
        return self._dim
    
    def rendered(self):
        return self._img
        
    def frame(self):
        return self._frame
        
    def velocity(self):
        return self._velocity
        
    def done(self):
        return self._frame >= self._img.width()
        
    # Constructors 
    def __init__(self, text, anchor, dim, font="spaceage",):
        self._font = font
        self._anchor = anchor
        self._dim = dim
        self._frame = -dim[0]
        self._velocity = 2
        
        font = Font.getFont(font)
        self._img = font.renderText(text)
        
    # Rendering
    def render(self, context):
        buffer = context.frameBuffer()
        
        if (self._frame < 0):
            offsetX = int(-self._frame)
            frame = 0
            width = int(self._dim[0] + self._frame)
        else:
            frame = int(self._frame)
            offsetX = 0;
            width = self._dim[0]
            # Adjust the width for the trailing bit
            if (frame > (self._img.width() - width)):
                width = (self._img.width() - frame)
                if (width < 0):
                    return;
                    
        buffer.copyEx(self._img, frame, 0, self._anchor[0] + offsetX, self._anchor[1],
            width, self._dim[1])
    
        self._frame = self._frame + self._velocity
    
        pass