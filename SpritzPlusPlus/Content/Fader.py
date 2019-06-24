import Zero
import Events
import Property
import VectorMath

import Action #Actions 

Vec4 = VectorMath.Vec4
Vec3 = VectorMath.Vec3

class Fader:
    DebugMode = Property.Bool(default = False)
    defaultOpacity = Property.Float(default = 1)
    FadeInDuration = Property.Float(default = 1)
    FadeOutDuration = Property.Float(default = 1)
    FadeInOnCreation = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        #clear any actions that might be lingering
        self.Owner.Actions.Cancel();
        
        currentColor = self.Owner.Sprite.Color
        self.Owner.Sprite.Color = Vec4(currentColor.r, currentColor.g, currentColor.b, self.defaultOpacity)
        self.TargetFade = self.defaultOpacity
        
        if self.FadeInOnCreation:
            self.FadeIn()
        
    
    def onUpdate(self, uEvent):
        pass
        
    #end onUpdate()
    
    def FadeOut(self, time = None):
        if not time:
            time = self.FadeOutDuration
        
        target = self.Owner.Sprite
        current = self.Owner.Sprite.Color
        endColor = Vec4( current.r, current.g, current.b, 0)
        
        seq = Action.Sequence(self.Owner)
        Action.Property(seq, target, "Color",end=endColor, duration=time)
        
    def FadeIn(self, time = None):
        if not self.Owner:
            return
        
        if not time:
            time = self.FadeInDuration
        
        if self.Owner.Sprite:
            self.Owner.Sprite.Visible = True
            self.Owner.Sprite.Color *= VectorMath.Vec4(1,1,1,0)
        #endif
        
        target = self.Owner.Sprite
        current = self.Owner.Sprite.Color
        endColor = Vec4( current.r, current.g, current.b, self.defaultOpacity)
        
        seq = Action.Group(self.Owner)
        
        Action.Property( seq, target, property="Color",end=endColor,duration=time )

Zero.RegisterComponent("Fader", Fader)