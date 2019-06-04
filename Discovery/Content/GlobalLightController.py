import Zero
import Events
import Property
import VectorMath

class GlobalLightController:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass
    
    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, "UnpowerEvent", self.onUnpower)
        Zero.Connect(self.Space, "PowerEvent", self.onPower)
        pass
    
    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onPower(self, pEvent):
        self.Owner.Light.Intensity = 0 #bad do this right later
        #raise
    
    def onUnpower(self, pEvent):
        self.Owner.Light.Intensity = 0.25
        #raise

Zero.RegisterComponent("GlobalLightController", GlobalLightController)