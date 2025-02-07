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

from abc import *

class Scene(ABC):
    @abstractmethod
    def render(self, context):
        pass;

class StatefulScene(Scene):
    
    # Constructors
    
    def __init__(self, state=0):
        self._state = state
        self._stateFrameCount = 0
        
    # State Management
        
    def currentState(self):
        return self._state
        
    def stateFrameCount(self):
        return self._stateFrameCount
        
    def setState(self, state):
        self._state = state
        self._stateFrameCount = 0
        
    def nextState(self):
        self._state = self._state + 1
        self._stateFrameCount = 0
        
    def stateFramesElapsed(self, limit):
        return self._stateFrameCount >= limit
        
        
    # Rendering
    
    @abstractmethod
    def onRenderState(self, context, state):
        pass
        
    def render(self, context):
        self.onRenderState(context, self._state)
        self._stateFrameCount = self._stateFrameCount + 1