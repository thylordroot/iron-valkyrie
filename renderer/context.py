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

    def par(self): 
        return (4/3)/(1.6)
    
    def scaleFactors(self):
        par = self.par()
        if (par < 1):
            return (1, 1/par)
        else:
            return (par, 1)
    
    def dim(self):
        return self._frameBuffer.dim()
    
    def actualDim(self):
        f = self.scaleFactors()
        dim = self._frameBuffer.dim()
        return (int(f[0] * dim[0]), int(f[1] * dim[1]))

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
        
        # Now yield the frame; although the logical resolution of mode 13h is 
        # 320x200, it does not have square pixels. Physically, this needs to 
        # fit into 320x240, which means that we need to correct the image for a
        # PAR of 1/1.2
        scaleFactors = self.scaleFactors()
        return self._frameBuffer.scale(scaleFactors[0], scaleFactors[1])