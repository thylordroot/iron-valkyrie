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

from renderer.scene import Scene
from renderer.image import Image

class TitleScene(Scene):
    def __init__(self):
        self._background = Image.load("assets/png/title/background.png")
        print(self._background.dim())
        print(self._background.channels())

    def render(self, context):
        buffer = context.frameBuffer()
    
        # Copy background
        buffer.copy(self._background)
        
        if (context.framesElapsed() >= 300):
            buffer.fillRect(0, 0, buffer.width(), context.framesElapsed() - 300, (0, 0, 0))
    
        if (context.framesElapsed() >= 600):
            context.makeSceneDone()
            context.resetElapsed()
            
            