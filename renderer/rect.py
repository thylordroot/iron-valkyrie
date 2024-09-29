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

class Rect:

    # Properties
    
    def xBound(self):
        return self.x + self.width

    def yBound(self):
        return self.y + self.height
    
    def xRange(self):
        return range(self.x, self.x+self.width)
        
    def yRange(self):
        return range(self.y, self.y+self.height)
        
    def isDegenerate(self):
        return self.width <= 0 or self.height <= 0

    # Constructors
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # Clipping (1 rectangle)
    
    def _clipAdjustEx(srcX, srcY, srcWidth, srcHeight, reqX, reqY, reqWidth, reqHeight):
        # Calculate X offset adjustment
        xAdj = 0
        if (reqX < srcX):
            xAdj = -(reqX - srcX)
            
        # Calculate Y offset adjustment
        yAdj = 0
        if (reqY < srcY):
            yAdj = -(reqY - srcY)
        
        # Calculate width adjustment - here we need to take into account any
        # adjustment that has already occurred, so we need to add in the
        # anchor adjustment.
        widthAdj = -xAdj
        reqWidth += (reqX - srcX)
        if ((xAdj + reqWidth) > srcWidth):
            widthAdj += srcWidth - reqWidth
            
        heightAdj = -yAdj
        reqHeight += (reqY - srcY)
        if ((yAdj + reqHeight) > srcHeight):
            heightAdj += srcHeight - reqHeight
        
        return (xAdj, yAdj, widthAdj, heightAdj)
    
    def clipAdjustEx(self, x, y, width, height):
        return Rect._clipAdjustEx(self.x, self.y, self.width, self.height, 
            x, y, width, height)
        
    def clipAdjust(self, rhs):
        return self.clipAdjustEx(rhs.x, rhs.y, rhs.width, rhs.height)
        
    def clipEx(self, x, y, width, height):
        adj = self.clipAdjustEx(x, y, width, height)
        return Rect(x + adj[0], y + adj[1], width + adj[2],
            height + adj[3])
            
    def clip(self, rhs):
        return self.clipEx(rhs.x, rhs.y, rhs.width, rhs.height)
        
    # Clipping (2 rectangles)
    
    
    def _clip2AdjustEx(srcX, srcY, srcWidth, srcHeight, destX, destY,
        destWidth, destHeight, rsX, rsY, rdX, rdY, reqWidth, reqHeight):
        # Clip source
        adjSrc = Rect._clipAdjustEx(srcX, srcY, srcWidth, srcHeight,
            rsX, rsY, reqWidth, reqHeight)
        
        # Adjust destination
        reqWidth += adjSrc[2]
        reqHeight += adjSrc[3]
        
        # Clip destination
        adjDest = Rect._clipAdjustEx(destX, destY, destWidth, destHeight,
            rdX, rdY, reqWidth, reqHeight)
        
        return (adjSrc[0] + adjDest[0], adjSrc[1] + adjDest[1], 
            adjSrc[2] + adjDest[2], adjSrc[3] + adjDest[3],
            adjDest[0], adjDest[1])
    
    def clip2AdjustEx(self, destX, destY, destWidth, destHeight,
        rsX, rsY, rdX, rdY, reqWidth, reqHeight):
            return Rect._clip2AdjustEx(self.x, self.y, self.width, self.height,
                destX, destY, destWidth, destHeight, rsX, rsY, rdX, rdY, 
                reqWidth, reqHeight)
                
    def clip2Adjust(self, dest, rsX, rsY, rdX, rdY, reqWidth, reqHeight):
        return self.clip2AdjustEx(target.x, target.y, dest.x, dest.y,
            dest.width, dest.height, rsX, rsY, rdX, rdY, reqWidth, reqHeight)
               
    def clip2Ex(self, destX, destY, destWidth, destHeight,
        rsX, rsY, rdX, rdY, reqWidth, reqHeight):
        adj = self.clip2AdjustEx(destX, destY, destWidth, 
            destHeight, rsX, rsY, rdX, rdY, reqWidth, reqHeight)
        return (Rect(rsX + adj[0], rsY + adj[1], reqWidth + adj[2], reqHeight + adj[3]),
            Rect(rdX + adj[4], rdY + adj[5], reqWidth + adj[2], reqHeight + adj[3]))
            
    def clip2(self, dest, rsX, rsY, rdX, rdY, width, height):
        return self.clip2Ex(dest.x, dest.y, dest.width, dest.height, 
            rsX, rsY, rdX, rdY, width, height)       
               
    def trim(self, vector):
        return Rect(self.x + vector[0], self.y + vector[1],
            self.width + vector[2], self.height + vector[3]);
               
    # Conversion
    
    def __str__(self):
        return "[x={x}, y={y}, width={width}, height={height}]".format(
            x=self.x, y=self.y, width=self.width, height=self.height)