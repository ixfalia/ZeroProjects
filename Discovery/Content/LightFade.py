import Zero
import Events
import Property
import VectorMath

class LightFade:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.isVisible = Property.Bool(default = True)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        #Zero.Connect(self.Space, "FadeEvent", self.onFadeSpace)
        Zero.Connect(self.Owner, "FadeEvent", self.onFade)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onFade(self, fEvent):
        if self.isVisible:
            self.fadeOut()
        else:
            self.fadeIn()
    
    def fadeOut():
        pass
    
    def fadeIn():
        pass

Zero.RegisterComponent("LightFade", LightFade)