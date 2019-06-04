import Zero
import Events
import Property
import VectorMath

import Action

class CelebrationMessage:
    EventType = Property.String()
    OwnerEvent = Property.Bool(default = False)
    SpaceEvent = Property.Bool(default = True)
    Duration = Property.Float(default = 4.0)
    Message = Property.String()
    
    def Initialize(self, initializer):
        if not self.EventType == "":
            if self.SpaceEvent:
                Zero.Connect(self.Space, self.EventType, self.onEvent)
            if self.OwnerEvent:
                Zero.Connect(self.Space, self.EventType, self.onEvent)
            #endif
        #endif
        
        if self.Message == "":
            if self.Owner.SpriteText:
                self.Message = self.Owner.SpriteText.Text
        
        self.reset()
    
    def onEvent(self, eEvent):
        print("CelebrationMessage.Celebrate(): WOO~!")
        if self.Owner.SpriteText:
            self.Owner.SpriteText.Visible = True
        if self.Owner.Sprite:
            self.Owner.Sprite.Visible = True
        
        self.Owner.SphericalParticleEmitter.Active = True
        
        seq =  Action.Sequence(self.Owner)
        Action.Delay(seq, self.Duration)
        Action.Call(seq, self.reset)
    
    def reset(self):
        if self.Owner.SpriteText:
            self.Owner.SpriteText.Visible = False
            self.Owner.SpriteText.Text = self.Message
        
        if self.Owner.Sprite:
            self.Owner.Sprite.Visible =  False
        
        self.Owner.SphericalParticleEmitter.Active = False

Zero.RegisterComponent("CelebrationMessage", CelebrationMessage)