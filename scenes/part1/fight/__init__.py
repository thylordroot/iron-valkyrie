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
from .starfield import Starfield
from random import randrange


class FightScene(StatefulScene):
    scrollerText = "Oh no! The Iron Valkyrie has been ambushed! Strange bird-like ships with what appear to be birds piloting them are opening fire on our intrepid hero. "
    
    # Constructors
    
    def __init__(self):
        super().__init__()
        
        # Load Images 
        shipFront = Atlas.load("assets/png/part1/spaceship-side.png", 64, 48, 2)
        bigBird = Atlas.load("assets/png/part1/fight/big-bird.png", 128, 64, 2)
        
        # Set up transitions
        self._inTransition = SquaresTransition(False)
        self._outTransition = SquaresTransition(True)
        
        # Set up scrollers
        self._textScroller = TextScroller(FightScene.scrollerText,
            (0, 0), (320, 16))
        self._textScroller2 = TextScroller("Wait, what is that thing?! Its huge!",
            (0, 0), (320, 16))
            
        # Set up sprites
        self._ship = Sprite(shipFront, True)
        self._ship.pos((0, 100-32))
        self._bigBird = Sprite(bigBird, False)
        self._starField = Starfield(320, 184, 16, 3, 100)
        scouts = []
        for i in range(0, 8):
            scouts.append(Scout())
        self._scouts = scouts
        
    def _transitionIn(self, context, buffer):
        self._inTransition.render(context)
        
        if (self.stateFramesElapsed(30)):
            self.nextState()
        
    def _doScouts(self, context, buffer):
        maxScouts = int(self.stateFrameCount() / 60);
        if (maxScouts >= 8):
            maxScouts = 7;
            
        
        for i in range(0, maxScouts+1):
            scout = self._scouts[i]
            if (not scout.enabled()):
                scout.pos((320, 100))
                scout.enabled(True)
                scout.velocity((-4, randrange(-16, 16)/8))
            
            scout.renderAndUpdate(buffer)
            # Recycle sprites that are off screen
            if (scout.x() < -scout.width() or scout.y() < -scout.height() 
                or scout.y() > buffer.height() + scout.height()):
                scout.enabled(False)
        
        self._textScroller.render(context)
        if (self._textScroller.done()):
            self._bigBird.enabled(True)
            self.nextState()
            
    def _clearScouts(self, context, buffer):
        count = 0;
        for i in range(0, 8):
            scout = self._scouts[i]
            if (scout.enabled()):
                scout.renderAndUpdate(buffer)
                # Recycle sprites that are off screen
                if (scout.x() < -scout.width() or scout.y() < -scout.height() 
                    or scout.y() > buffer.height() + scout.height()):
                    scout.enabled(False)
                count += 1
        if (count == 0):
            self._bigBird.enabled(True)
            self._bigBird.pos((320, 100-32)) 
            self.nextState()
            
    def _renderBigBird(self, context, buffer):
        self._bigBird.render(buffer)
        self._bigBird.advanceFrame()
        
        if (self._bigBird.x() > 160):
            self._bigBird.x(self._bigBird.x() - 1)
    
        self._textScroller2.render(context)
        if (self._textScroller2.done()):
            self.nextState()
            
    def _transitionOut(self, context, buffer):
        self._ship.pos((
            self._ship.x() + 1,
            self._ship.y() + 1
        ))
        self._outTransition.render(context)
        if (self.stateFramesElapsed(60)):
            context.makeSceneDone()

    def onRenderState(self, context, state):
        buffer = context.frameBuffer()
        
        buffer.fillRect(0, 0, 320, 200, (0,0,0))
        self._starField.renderAndUpdate(buffer)
        
        self._ship.render(buffer)
        self._ship.advanceFrame()
        
        # Now select state handler
        match(state):
            case 0:
                self._transitionIn(context, buffer)
            case 1:
                self._doScouts(context, buffer)
            case 2:
                self._clearScouts(context, buffer)
            case 3:
                self._renderBigBird(context, buffer)
            case 4:
                self._transitionOut(context, buffer)
                
        
        