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

from renderer import Scene

class SquaresTransition(Scene):

    # Constructors

    def __init__(self, out=True):
        self._out = out;
        self._tileSz = 8
        self._tileFrames = int(self._tileSz/2)
        self._localFrameCount = 0
        self._divisor = 4;
    
    # Rendering
    
    def _renderTile(self, buffer, x, y, frame):
        if (frame > self._tileFrames):
            frame = self._tileFrames;
        elif (frame < 0):
            frame = 0
    
        width = frame;
        offset = (self._tileFrames) - frame;
    
        if (not self._out):
            width = offset
            offset = frame;
            
        x = x + offset
        y = y + offset
        
        width = width * 2
        
        buffer.fillRect(x, y, width, width, (0, 0, 0))
        
    def render(self, context):
        buffer = context.frameBuffer()
        
        counter = 0;
        for y in range(0,buffer.height(),self._tileSz):
            for x in range(0,buffer.width(),self._tileSz):
                frame = .self_localFrameCount - counter 
                self._renderTile(buffer, x, y, 
                    int((frame/self._divisor))
                counter = (counter + 1) % (self._tileFrames)
                
        self._localFrameCount = self._localFrameCount + 1