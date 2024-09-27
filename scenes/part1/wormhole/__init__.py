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
from renderer.atlas import Atlas
from renderer.sprite import Sprite
from renderer.textscroller import TextScroller
from renderer.transition.squares import SquaresTransition

class WormholeScene(Scene):
    scrollerText = "Why render multiple frames when you can cheat and use palette cycling? The below image is really a single frame. Unfortunately, I had to hack at it a little because the renderer uses BGR and not indexed mode. Still makes for a pretty neat effect."
    
    _srcColors = [
            (0x00, 0x00, 0x00),
            (0x33, 0x33, 0x33),
            (0x55, 0x55, 0x55),
            (0x77, 0x77, 0x77),
            (0x99, 0x99, 0x99),
            (0xAA, 0xAA, 0xAA),
            (0xCC, 0xCC, 0xCC),
            (0xFF, 0xFF, 0xFF)
        ]
    
    _backgroundColors = [
            (0x00, 0x00, 0x00),
            (0x55, 0x00, 0x00),
            (0xAA, 0x00, 0x00),
            (0xff, 0x41, 0x33),
            (0xff, 0x82, 0x00),
            (0xff, 0xbe, 0x00),
            (0xFF, 0x9e, 0x82),
            (0xFF, 0xCA, 0xBA),
        ]
    
    def _makeBackgroundAtlas():
        src = Image.load("assets/png/part1/wormhole/background.png");
        
        # We're not really set up to do palette swapping, so let's 
        # simulate it here by producing an atlas.
        dest = Image.create(src.width()*len(WormholeScene._srcColors), src.height())
        offset = 0;
        
        # Create the color map which we will cycle
        colorMap = [*WormholeScene._backgroundColors]

        # Prerender the frames
        for i in range(0,len(colorMap)):
            frame = src.clone()
            frame.replace(WormholeScene._srcColors, colorMap)
        
            dest.copyEx(frame, 0, 0, i * src.width(), 0, src.width(), src.height()) 
            colorMap.append(colorMap.pop(0));
            
        return Atlas(dest, src.width(), src.height(), 8)
    
    # Constructors
    
    def __init__(self):
        self._background = WormholeScene._makeBackgroundAtlas()
    
        self._textScroller = TextScroller(WormholeScene.scrollerText,
            (0, 0), (320, 16))
          
    # Rendering
    
    def render(self, context):
        buffer = context.frameBuffer()
        
        frame = int((context.framesElapsed() % (4*self._background.count()))/4)
        self._background.copy(buffer, frame, 0, 16)  
        self._textScroller.render(context)
        
        if (self._textScroller.done()):
            context.makeSceneDone()