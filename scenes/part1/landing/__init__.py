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
from renderer.atlas import Atlas
from renderer.font import Font
from renderer.sprite import Sprite
from renderer.textscroller import TextScroller
from renderer.transition.squares import SquaresTransition


class LandingScene(StatefulScene):

    # Constructors
    
    def __init__(self):
        super().__init__()
        
        # Load Images 
        self._background = Image.load("assets/png/part1/landing/amadacron.png")
        shipFront = Atlas.load("assets/png/part1/spaceship-side.png", 64, 48, 2)
        
        shipLarge = Atlas.load("assets\png\part1\spaceship-back.png", 64, 48, 2)
        shipSmall = Atlas.load("assets\png\part1\landing\spaceship-small.png", 32, 24, 2)
        shipTiny = Atlas.load("assets\png\part1\landing\spaceship-tiny.png", 16, 12, 2)
        
        self._font = Font.getFont("spaceage")
        
        # Set up transitions
        self._inTransition = SquaresTransition(False)
        self._outTransition = SquaresTransition(True)
            
        # Set up sprites
        self._shipLarge = Sprite(shipLarge, True)
        self._shipLarge.pos((160-32, 100-12))
        self._shipSmall = Sprite(shipSmall, False)
        self._shipSmall.pos((160-16, 100-6))
        self._shipTiny = Sprite(shipTiny, False)
        self._shipTiny.pos((160-8, 100-3))
        
        
    def _transitionIn(self, context, buffer):
        self._shipLarge.render(buffer)
        self._inTransition.render(context)
        self._shipLarge.advanceFrame()
        
        if (self.stateFramesElapsed(60)):
            self.nextState()
        
    def _small(self, context, buffer):
        self._shipSmall.render(buffer)
        self._shipSmall.advanceFrame()
        
        if (self.stateFramesElapsed(30)):
            self.nextState()
            
    def _tiny(self, context, buffer):
        self._shipTiny.render(buffer)
        self._shipTiny.advanceFrame()
        
        if (self.stateFramesElapsed(15)):
            self.nextState()
           
    def _planetName(self, context, buffer):
        self._font.render("Planet", buffer, 112, 16, True)
        self._font.render("Amadacron", buffer, 88, 184, True)
        if (self.stateFramesElapsed(120)):
            self.nextState()
            
    def _transitionOut(self, context, buffer):
        self._outTransition.render(context)
        if (self.stateFramesElapsed(60)):
            context.makeSceneDone()

    def onRenderState(self, context, state):
        buffer = context.frameBuffer()
        
        # Copy background
        buffer.copy(self._background)
        
        # Now select state handler
        match(state):
            case 0:
                self._transitionIn(context, buffer)
            case 1:
                self._small(context, buffer)
            case 2:
                self._tiny(context, buffer)
            case 3:
                self._planetName(context, buffer)
            case 4:
                self._transitionOut(context, buffer)