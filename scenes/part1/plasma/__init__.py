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
from perlin_noise import PerlinNoise
import math

def _lerp(x, y, t):
    return (x*(1-t)) + y*t
    
def _lerpColor(x, y, t):
    return (
        _lerp(x[0], y[0], t),
        _lerp(x[1], y[1], t),
        _lerp(x[2], y[2], t)
    )
    
def _createSrcColors(n):
    ret = []
    offset = int(256/n);
    for i in range(0, n):
        color = i*offset
        if (color > 255):
            color = 255;
        ret.append((color, color, color))
    print(len(ret))
    return ret;
    
def _createBackgroundColors(n, *stops):
    ret = []
    tLimit = len(stops)-1
    tStep = len(stops)/n
    t = tStep;
    
    ret.append(stops[0])
    while (t < tLimit):
        offset = int(t)
        ret.append(_lerpColor(stops[offset], stops[offset+1], t - offset))
        t += tStep
    
    # We will probably end up with an odd 
    if ((n - len(ret)) > 2):
        left = n - len(ret) - 2;
        t = t - offset - tStep
        tStep /= left/2
        offset = int(t)-1
        
        
        print((t, left, tStep))
    
        while left > 0:
            ret.insert(0, _lerpColor(stops[0], stops[1], 1-t))
            left -= 1;
            if (left > 0):
                ret.append(_lerpColor(stops[offset], stops[offset+1], t))
                left -= 1
            t += tStep
    

    ret.insert(0, stops[0]) 
    ret.append(stops[int(t)])
    
    return ret

class PlasmaScene(Scene):
    scrollerText = "Every good demo needs a plasma. Here we use Perlin noise rather than the traditional Diamond Square method. We also use palette cycling here, but we use a broader palette of 128 colors."
    

    
    _srcColors = _createSrcColors(128)
    
    _backgroundColors = _createBackgroundColors(128, 
        (0x00, 0x00, 0x00), # 1
        (0xAA, 0x00, 0xAA), #2
        (0x00, 0x00, 0xFF), #3
        (0x00, 0xFF, 0xFF), #4
        (0xFF, 0xFF, 0xFF), #5
        (0xFF, 0x9e, 0x82), #6
        (0xff, 0x82, 0x00), #7
        (0x33, 0x00, 0x33) #8
        )
    
    def _makeBackgroundAtlas():
        noises = []
        weights = []
        for i in range(0, 4):
            j = i + 1
            noises.append(PerlinNoise(octaves=2.25*j, seed=12345+i))
            weights.append(1.0/(1 << i));
            print(weights)
    
        src = Image.create(320, 184);
        # Now generate plasma
        xStep = 1.0/320
        yStep = 1.0/184
        
        # Create the color map which we will cycle
        colorMap = [*PlasmaScene._backgroundColors]

        print("Rendering plasma...")
        for y in range(0, 184):
            yF = y * yStep
            for x in range(0, 320):
                xF = x * xStep
                sample = 0;
                for i in range(0, len(noises)):
                    sample += weights[i] * noises[i]([yF, xF])
                
                sample += 0.5
                
                if (sample < 0):
                    sample = 0
                else:
                    sample = int(sample * len(colorMap))
                    if (sample >= len(colorMap)):
                        sample = len(colorMap) - 1
                
                color = PlasmaScene._srcColors[sample]
                src._img[y, x] = color
        
        src.save("foo.png")
        
        # We're not really set up to do palette swapping, so let's 
        # simulate it here by producing an atlas.
        frames = int(len(PlasmaScene._srcColors)/2)
        dest = Image.create(src.width()*frames, src.height())
        offset = 0;
        
        
        # Prerender the frames
        for i in range(0,frames):
            print(" {i}".format(i=i))
            frame = src.clone()
            frame.replace(PlasmaScene._srcColors, colorMap)
        
            dest.copyEx(frame, 0, 0, i * src.width(), 0, src.width(), src.height()) 
            colorMap.append(colorMap.pop(0));
            colorMap.append(colorMap.pop(0));
            
        print(frames)
        return Atlas(dest, src.width(), src.height(), frames)
    
    # Constructors
    
    def __init__(self):
        self._background = PlasmaScene._makeBackgroundAtlas()
    
        self._textScroller = TextScroller(PlasmaScene.scrollerText,
            (0, 0), (320, 16))
            
        shipAtlas = Atlas.load("assets\png\part1\spaceship-back.png", 64, 48, 2)
        self._ship = Sprite(shipAtlas, True)
        self._ship.x(160-32)
          
    # Rendering
    
    def render(self, context):
        buffer = context.frameBuffer()
        
        frame = int((context.framesElapsed() % self._background.count()))
        self._background.copy(buffer, frame, 0, 16)  
        self._textScroller.render(context)
        
        # Now render the ship
        angle = (context.framesElapsed() % 60) * ((2*math.pi)/60)
        self._ship.y(100-12 + int(math.sin(angle)*5));
        self._ship.render(buffer);
        self._ship.advanceFrame();
        
        if (self._textScroller.done()):
            context.makeSceneDone()