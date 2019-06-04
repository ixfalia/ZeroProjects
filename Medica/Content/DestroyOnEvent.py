import Zero
import Events
import Property
import VectorMath

class DestroyOnEvent:
    EventToDetect = Property.String()
    Active = Property.Bool(default = True)
    
    def Initialize(self, initializer):
        if self.EventToDetect:
            Zero.Connect(self.Space, self.EventToDetect, self.onEvent)
            Zero.Connect(self.Owner, self.EventToDetect, self.onEvent)
    
    def onEvent(self, e):
        if self.Active:
            self.Owner.Destroy()

Zero.RegisterComponent("DestroyOnEvent", DestroyOnEvent)