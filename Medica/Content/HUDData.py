import Zero
import Events
import Property
import VectorMath

class HUDData:
    Name = Property.String()
    
    def Initialize(self, initializer):
        e = Zero.ScriptEvent()
        e.Name = self.Name
        e.Object = self.Owner
        Zero.Game.DispatchEvent("HUDRegisterEvent", e)

Zero.RegisterComponent("HUDData", HUDData)