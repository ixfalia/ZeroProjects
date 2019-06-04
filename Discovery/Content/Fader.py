import Zero
import Events
import Property
import VectorMath

import Action

class Fader: #only handles sprites and models
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.FadeChildren = Property.Bool(default = True)
        self.FadeInOnStart = Property.Bool(default = False)
        
        self.FadeInTime = Property.Float(default = 0.25)
        self.FadeOutTime = Property.Float(default = 0.25)
        self.startingAlpha = Property.Float()
        pass

    def Initialize(self, initializer):
        self.FadeInDuration = 0.5
        self.FadeOutDuration = 0.5
        
        
        if self.Owner.ColorBase:
            self.StartingColor = self.Owner.ColorBase.Color
        elif self.Owner.Sprite:
            self.StartingColor = self.Owner.Sprite.Color
        elif self.Owner.Model:
            self.StartingColor = self.Owner.Model.Color
        
        self.sequence = Action.Sequence(self.Owner)
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def fadeIn(self):
        if self.FadeChildren:
            self.childrenFadeIn()
        self.sequence.cancel()
        

Zero.RegisterComponent("Fader", Fader)