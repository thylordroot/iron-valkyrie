#!/usr/bin/env python3

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

from renderer import VideoRenderer, Font
from scenes import *

Font.bootstrapFonts()


renderer = VideoRenderer("test.mp4");

# Render Part 1
#renderer.renderScenes(TitleScene());

# Render Part 2
renderer.renderScenes(*[part2.PlanetfallScene()])

renderer.close();