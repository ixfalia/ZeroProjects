import Zero
import Events
import Property
import VectorMath

import Action

class Lifetime:
    Duration = Property.Float(default = 4)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        self.timer = 0
    
    def onUpdate(self, uEvent):
        self.timer += uEvent.Dt
        
        if not self.Owner:
            return
        
        if self.timer >= self.Duration:
            if self.Owner.Fader:
                self.Owner.Fader.FadeOut()
                seq = Action.Sequence(self.Owner)
                Action.Delay(seq, self.Owner.Fader.FadeOutDuration)
                Action.Call(seq, self.Owner.Destroy)
            else:
                self.Destroy()

Zero.RegisterComponent("Lifetime", Lifetime)