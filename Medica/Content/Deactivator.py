import Zero
import Events
import Property
import VectorMath

class Deactivator:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "FreezeEvent", self.onFreeze)
        Zero.Connect(self.Space, "UnfreezeEvent", self.onUnfreeze)
        
        Zero.Connect(self.Space, "PauseEvent", self.onFreeze)
        Zero.Connect(self.Space, "UnpauseEvent", self.onFreeze)
    
    def onFreeze(self, e):
        nEvent = Zero.ScriptEvent()
        self.Owner.DispatchEvent("InactiveEvent", nEvent)
    
    def onUnfreeze(self, e):
        nEvent = Zero.ScriptEvent()
        self.Owner.DispatchEvent("ReactivateEvent", nEvent)

Zero.RegisterComponent("Deactivator", Deactivator)