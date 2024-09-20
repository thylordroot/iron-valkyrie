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

from .context import RenderContext
import cv2;

class VideoRenderer:

    # Properties
    
    

    # Constructors

    def __init__(self, path):
        self._context = RenderContext()
        self._writer = cv2.VideoWriter(path, 
            cv2.VideoWriter_fourcc(*"mp4v"),
            self._context.fps(), self._context.dim())
        
    # Rendering
    
    def _renderSceneFrame(self, scene):
        self._context.renderScene(scene)
        self._writer.write(self._context.frameBuffer()._img)
        if (self._context.sceneDone()):
            self._context._sceneDone = False
            return False
        else:
            return True

    def renderScenes(self, *args):
        for scene in args:
            while self._renderSceneFrame(scene):
                pass
            
    
    def close(self):
        self._writer.release()