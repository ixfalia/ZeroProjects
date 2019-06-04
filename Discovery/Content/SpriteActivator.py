import Zero
import Events
import Property
import VectorMath

class SpriteActivator:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "ActivateEvent", self.onActivate)
        Zero.Connect(self.Owner, "DeactivateEvent", self.onDeactivate)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onActivate(self, aEvent):
        self.Owner.Sprite.Visible = True
    
    def onDeactivate(self, aEvent):
        self.Owner.Sprite.Visible = False

Zero.RegisterComponent("SpriteActivator", SpriteActivator)