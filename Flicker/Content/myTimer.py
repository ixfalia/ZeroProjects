import Zero
import Events
import Property
import VectorMath

class myTimer:
    registry = []
    timer = 0
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
    
    def onUpdate(self, Event):
        self.timer += Event.Dt

Zero.RegisterComponent("myTimer", myTimer)