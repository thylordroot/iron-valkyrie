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
from renderer.sprite import Sprite
from renderer.textscroller import TextScroller
from renderer.transition.squares import SquaresTransition
from .scout import Scout


class FightScene(StatefulScene):
    scrollerText = "Oh no! The Iron Valkyrie has been ambushed! Strange bird-like ships with what appear to be birds piloting them are opening fire on our intrepid hero. "
    
    # Constructors
    
    def __init__(self):
        super().__init__()
        
        # Load Images 
        shipFront = Atlas.load("assets/png/part1/spaceship-side.png", 64, 48, 2)
        bigBird = Atload.load("assets/png/part1/fight/big-bird.png", 128, 64, 2)
        
        # Set up transitions
        self._inTransition = SquaresTransition(False)
        self._outTransition = SquaresTransition(True)
        
        # Set up scrollers
        self._textScroller = TextScroller(FightScene.scrollerText,
            (0, 0), (320, 16))
            
        # Set up sprites
        self._ship = Sprite(shipFront, True)
        self._bigBird = Sprite(bigBird, False)
        scouts = []
        for i in range(0, 8):
            scouts.append(Scout())
        
    def _transitionIn(self, context, buffer):
        self._inTransition.render(context)
        
        if (self.stateFramesElapsed(30)):
            self.nextState()
        
    def _doScouts(self, context, buffer):
        if (self.stateFramesElapsed(1200)):
            self.nextState()
            
    def _transitionOut(self, context, buffer):
        
    
    
        self._outTransition.render(context)
        if (self.stateFramesElapsed(60)):
            context.makeSceneDone()

    def onRenderState(self, context, state):
        buffer = context.frameBuffer()
        
        # Now select state handler
        match(state):
            case 0:
                self._transitionIn(context, buffer)
            case 1:
                self._doScouts(context, buffer)
            case 2:
                self._transitionOut(context, buffer)
            
        if (state != 0):
            self._textScroller.render(context)