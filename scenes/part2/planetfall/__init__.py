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
from renderer.font import Font
from renderer.transition.squares import SquaresTransition

class PlanetfallScene(StatefulScene):
    introText = "Somewhere, on the planet below."


    def __init__(self):
        super().__init__()
        
        # Load images
        self._background = Image.load("assets/png/part2/planetfall/background.png")
        
        # Set up transitions
        self._inTransition = SquaresTransition(False)
        self._outTransition = SquaresTransition(True)
        self._font = Font.getFont("spaceage")
        
    def _renderBackground(self, context, buffer):
        position = int(context.framesElapsed()/2)
        
        # Determine where in the scene we are
        if (position < 200):
            position = 200 - position
        else:
            position = 0
            
        buffer.copyEx(self._background, 0, position, 0, 0,
            buffer.width(), buffer.height())

    def _renderFlavorText(self, context, buffer):
        self._font.render("Somewhere on the", buffer, 32, 92)
        self._font.render("planet below.", buffer, 64, 108)

    def _flavorText(self, context, buffer):
        self._renderFlavorText(context, buffer)
        if (self.stateFramesElapsed(120)):
            self.nextState()
            
    def _flavorTextTransition(self, context, buffer):
        self._renderFlavorText(context, buffer)
        self._outTransition.render(context)
        if (self.stateFramesElapsed(120)):
            context.resetElapsed()
            self._outTransition.reset()
            self.nextState()
     
    def _transitionIn(self, context, buffer):
        self._inTransition.render(context)
        if (self.stateFramesElapsed(240)):
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
        if (state > 1):
            self._renderBackground(context, buffer)
        
        # Now select state handler
        match(state):
            case 0:
                self._flavorText(context, buffer)
            case 1:
                self._flavorTextTransition(context, buffer)
            case 2:
                self._transitionIn(context, buffer)
            case 3:
                self._crash(context, buffer)
            case 4:
                self._parachute(context, buffer)
            case 5:
                self._transitionOut(context, buffer)
            
            