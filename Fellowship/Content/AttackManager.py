import Zero
import Events
import Property
import VectorMath

class AttackManager:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass

Zero.RegisterComponent("AttackManager", AttackManager)