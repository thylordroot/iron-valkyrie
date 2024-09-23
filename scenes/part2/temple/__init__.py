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

class TempleScene(StatefulScene):
    scrollerText = "Sorry Amada, your likeness has been sacrificed for the good of us all. So you can hold the best core. What core is that? Why surge core, of course! Who better to be the bearer of surge core than yourself, its biggest fan? Magnet core may be fun for a while, but it will leave your soul empty inside. Phazon core will leave you a dry husk. But surge core, it is your one dependable friend that will never leave you. Harvest and equip surge core as soon as you can, and you will find yourself winning all of the time. Because surge core is hard required in this seed, it is the core you need."

    coreColors = [
        (0x00, 0x00, 0xAA), # Surge
        (0x00, 0xFF, 0xFF), # Magnet
        (0x00, 0xAA, 0x00), # Aegis
        (0xFF, 0xFF, 0x00), # Phazon
        (0xAA, 0x00, 0xAA), # Crystal
        (0xAA, 0xAA, 0xAA), # Chrono
        (0x55, 0x55, 0x55), # Shadow
    ]

    def _renderCoreAtlas(src, color):
        img = src.clone();
        
        buffer = img._img;
        mask = (buffer[:,:,0] == 0xFF) & (buffer[:,:,1] == 0xFF) & (buffer[:,:,2] == 0xFF)
        
        buffer[:,:,0:3][mask] = color
    
        return Atlas(img, 16, 16, 16)

    def _renderCoreSprites(src):
        ret = []
        for color in TempleScene.coreColors:
            atlas = TempleScene._renderCoreAtlas(src, color)
            
            ret.append(Sprite(atlas))
        return ret

    def __init__(self):
        super().__init__()
        
        # Load Images 
        self._background = Image.load("assets/png/part2/temple/background.png")
        tinyCore = Image.load("assets/png/part2/temple/surge-tiny.png")
        core = Image.load("assets/png/part2/temple/core.png")
        
        # Set up transitions
        self._inTransition = SquaresTransition(False)
        self._outTransition = SquaresTransition(True)
        
        # Set up scrollers
        self._textScroller = TextScroller(TempleScene.scrollerText,
            (0, 184), (320, 16))
            
        # Set up sprites
        self._tinyCore = Sprite(tinyCore, True)
        self._tinyCore.pos((156, 74))
        self._core = TempleScene._renderCoreSprites(core)
        
    def _transitionIn(self, context, buffer):
        self._tinyCore.render(buffer)
        self._inTransition.render(context)
        
        if (self.stateFramesElapsed(30)):
            self.nextState()
        
    def _await(self, context, buffer):
        self._tinyCore.render(buffer)
        if (self.stateFramesElapsed(1200)):
            self.nextState()
            
    def _tinyCoreRise(self, context, buffer):
        self._tinyCore.y(self._tinyCore.y() - 1)
        self._tinyCore.render(buffer)
        if (self.stateFramesElapsed(300)):
            self._tinyCore.enabled(False)
            self.nextState()
            
    def _descendSurgeCore(self, context, buffer):
        surgeCore = self._core[0]
        if (self.stateFrameCount() == 1):
            surgeCore.pos((152, -16))
            surgeCore.enabled(True)
        
        if (self.stateFrameCount() % 2 == 1):
            surgeCore.advanceFrame()
        
        surgeCore.y(surgeCore.y() + 1)
        surgeCore.render(buffer)
        if (self.stateFramesElapsed(86)):
            self.nextState()
        
        
        
    def _waitForDone(self, context, buffer):
        surgeCore = self._core[0]
        
        if (self.stateFrameCount() % 2 == 1):
            surgeCore.advanceFrame()
        surgeCore.render(buffer)
        
        if (self._textScroller.done()):
            self.nextState()
        
    def _transitionOut(self, context, buffer):
        surgeCore = self._core[0]
    
        if (self.stateFrameCount() % 2 == 1):
            surgeCore.advanceFrame()
        surgeCore.render(buffer)
    
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
                self._await(context, buffer)
            case 2:
                self._tinyCoreRise(context, buffer)
            case 3:
                self._descendSurgeCore(context, buffer)
            case 4:
                self._waitForDone(context, buffer)
            case 5:
                self._transitionOut(context, buffer)
            
        if (state != 0):
            self._textScroller.render(context)