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

import numpy;
from random import randrange

class Starfield:
    # Properties
    def layers(self):
        return len(self._layers)

    # Constructors
    
    def __init__(self, width, height, offset, layers = 3, n = 100):
        self._width = width;
        self._height = height;
        self._offset = offset;
        self._n = n
        layerData = []
        
        # Build up each layers
        for i in range(0, layers):
            layer = numpy.zeros((n, 2), numpy.int16)
            # Now fill with random values
            for j in range(0, n):
                layer[j, 0] = randrange(0, width)
                layer[j, 1] = randrange(0, height)
            layerData.append(layer)
        
        self._layers = layerData
        
    def renderAndUpdate(self, buffer):
        velocity = self.layers()
        
        for layer in self._layers:
            for j in range(0, self._n):
                point = layer[j]
                buffer.fillRect(point[0], self._offset + point[1], 
                    1, 1, (0x77, 0x77, 0x77))
                point = (point[0] - velocity, point[1])
                if (point[0] < 0):
                    point = (
                        self._width - 1,
                        randrange(0, self._height)
                    )
                layer[j] = point
                
            velocity -= 1
        