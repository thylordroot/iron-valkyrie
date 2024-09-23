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
#    but WITHOUT ANY WARRANTY; without even t implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .atlas import Atlas
from .image import Image
from os.path import basename, splitext
import numpy
import glob

class Font:
    # Properties

    _fonts = None
    
    def width(self):
        return self._atlas.width()
    
    def height(self):
        return self._atlas.height()
    
    def dim(self):
        return self._atlas.dim()
    
    # Constructors
    
    def __init__(self, atlas):
        self._atlas = atlas
    
    def load(path, width, height, count=-1):
        return Font(Atlas.load(path, width, height, count))
        
    def bootstrapFonts():
        ret = dict()
        for f in glob.glob("assets/png/font/*.png"):
            name = splitext(basename(f))[0]
            font = Font.load(f, 16, 16)
            ret[name] = font
        Font._fonts = ret
        
    def getFont(name):
        if (Font._fonts == None):
            Font.bootstrapFonts()
        return Font._fonts[name]
        
    # Rendering
    
    def renderText(self, string):
        n = len(string)
        dim = self.dim()
        ret = Image.create(n * dim[0], dim[1], 4)
        
        string = string.upper()
        offset = 0;
        for c in string:
            char = (ord(c) - 32) & 0x3F
            self._atlas.copy(ret, char, offset, 0)
            offset = offset + dim[0]
            
        return ret
        
    def render(self, string, dest, x, y, compose = True):
        img = self.renderText(string);
        dest.copyEx(img, 0, 0, x, y, img.width(), img.height())
        
        