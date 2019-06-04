import Zero
import Events
import Property
import VectorMath

class EventDispatcher:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.LevelStarted, self.onLevel)
        pass
    
    def onLevel(self, e):
        pass
    

Zero.RegisterComponent("EventDispatcher", EventDispatcher)