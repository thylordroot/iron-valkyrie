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

from renderer.scene import StatefulScene
from renderer.image import Image
from renderer.transition.squares import SquaresTransition

class PlanetfallScene(StatefulScene):
    def __init__(self):
        super().__init__()
        self._background = Image.load("assets/png/part2/planetfall/background.png")
        self._outTransition = SquaresTransition(True)
        
    def _renderBackground(self, context, buffer):
        position = context.framesElapsed()
        
        # Determine where in the scene we are
        if (position < 200):
            position = 200 - position
        else:
            position = 0
            
        buffer.copyEx(self._background, 0, position, 0, 0,
            buffer.width(), buffer.height())
        
    def _transitionIn(self, context, buffer):
        print(self.stateFrameCount())
        if (self.stateFramesElapsed(120)):
            self.nextState()
        
    def _crash(self, context, buffer):
        if (self.stateFramesElapsed(120)):
            self.nextState()
        
    def _parachute(self, context, buffer):
        if (self.stateFramesElapsed(120)):
            self.nextState()
        
    def _transitionOut(self, context, buffer):
        self._outTransition.render(context)
        if (self.stateFramesElapsed(60)):
            context.makeSceneDone()

    def onRenderState(self, context, state):
        buffer = context.frameBuffer()
        
        # Copy background
        self._renderBackground(context, buffer)
        
        # Now select state handler
        match(state):
            case 0:
                self._transitionIn(context, buffer)
            case 1:
                self._crash(context, buffer)
            case 2:
                self._parachute(context, buffer)
            case 3:
                self._transitionOut(context, buffer)
            
            