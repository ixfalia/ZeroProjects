import Zero
import Events
import Property
import VectorMath

OrbTypes = Property.DeclareEnum("OrbTypes", ["KeyOrb", "FireOrb", "IceOrb"])

class OrbType:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.CurrentType = Property.Enum("OrbTypes")
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass

Zero.RegisterComponent("OrbType", OrbType)