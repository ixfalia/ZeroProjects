import Zero
import Events
import Property
import VectorMath

class SpaceEventDispatcher:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "SpaceCreated", self.onSpace)
        
        self.AllSpaces = {}
    
    def onSpace(self, sEvent):
        name = sEvent.Name
        space = sEvent.SpaceObject
        
        self.AllSpaces[name] = space
    
    def DispatchToAllSpaces(self, eventName, Event):
        for s in self.AllSpaces:
            s.DispatchEvent(Name, Event)
    
    def DispatchToSpace(self, SpaceName, eventName, Event):
        self.AllSpaces[SpaceName].DispatchEvent(Name, eventName)

Zero.RegisterComponent("SpaceEventDispatcher", SpaceEventDispatcher)