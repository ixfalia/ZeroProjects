import Zero
import Events
import Property
import VectorMath

class Activator:
    Activate = Property.String()
    Deactivate = Property.String()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, self.Activate, self.onActivate)
        Zero.Connect(self.Space, self.Deactivate, self.onDeactivate)
    
    def onActivate(self, e):
        self.Owner.DispatchEvent("ReactivateEvent", e)
    
    def onDeactivate(self, e):
        self.Owner.DispatchEvent("DeactivateEvent", e)

Zero.RegisterComponent("Activator", Activator)