import Zero
import Events
import Property
import VectorMath

import Action

class Popup:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Offset = Property.Vector3(default = VectorMath.Vec3())
        self.Duration = Property.Float(0.5)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        seq = Action.Sequence(self.Owner)
        pos = self.Owner.Transform.Translation
        Action.Property(seq, self.Owner.Transform, "Translation", pos + self.Offset, self.Duration)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass

Zero.RegisterComponent("Popup", Popup)