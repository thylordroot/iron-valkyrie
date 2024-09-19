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

class RenderContext:

    # Properties
    
    def frameBuffer(self):
        return self._frameBuffer

    def dim(self):
        return self._frameBuffer.dim()

    def totalFrames(self):
        return self._totalFrames
        
    def framesElapsed(self):
        return self._framesElapsed
        
    def fps(self):
        return self._fps
        
    def totalTimeSeconds(self):
        return (self._totalFrames)/(self._fps)
        
    def totalTime(self):
        seconds = self.totalTimeSeconds()
        hours = int (seconds / 3600)
        seconds = (seconds % 3600)
        minutes = int(seconds / 60)
        seconds = seconds % 60;
        return "{hours}:{minutes}:{seconds}".format(hours=hours, 
            minutes=minutes, seconds=seconds) 

    def sceneDone(self):
        return self._sceneDone

    # Constructors

    def __init__(self):
        self._frameBuffer = Image.create(320, 200)
        self._totalFrames = 0
        self._framesElapsed = 0
        self._fps = 60
        self._sceneDone = False
        
    # Rendering
    
    def makeSceneDone(self):
        self._sceneDone = True
    
    def resetElapsed(self):
        elapsed = 0;
    
    def renderScene(self, scene):
        scene.render(self)
        self._totalFrames = self._totalFrames + 1
        self._framesElapsed = self._framesElapsed + 1