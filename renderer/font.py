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
import glob

class Font:
    # Properties

    _fonts = dict()
    
    
    
    # Constructors
    
    def __init__(self, atlas):
        self._atlas = atlas
    
    def load(path, width, height, count=-1):
        return Font(Atlas.load(path, width, height, count))
        
    def bootstrapFonts():
        print(glob.glob("assets/png/font/*.png"))