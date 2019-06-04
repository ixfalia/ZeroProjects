import Zero
import Events
import Property
import VectorMath

import Action

class ShowAfterTime:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Delay = Property.Float()
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        seq = Action.Sequence(self.Owner)
        Action.Delay(seq, self.Delay)
        Action.Call(seq, self.Reveal)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def Reveal(self):
        if self.Owner.SpriteText:
            self.Owner.SpriteText.Visible = True
        if self.Owner.Sprite:
            self.Owner.Sprite.Visible = True

Zero.RegisterComponent("ShowAfterTime", ShowAfterTime)