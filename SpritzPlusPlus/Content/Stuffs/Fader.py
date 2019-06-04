import Zero
import Events
import Property
import VectorMath

class Fader:
    DebugMode = Property.Bool(default = False)
    FadeInDuration = Property.Float(default = 1)
    FadeOutDuration = Property.Float(default = 1)
    
    def Initialize(self, initializer):
        pass
        
    def FadeOut(self, me, target, time):
        seq = Action.Sequence(me)
        seq.Add( Action.Property( on=target, property="Color",end=Vec4(1,1,1,0),duration=time))
        
    def FadeIn(self, me, target, time):
        seq = Action.Sequence(me)
        seq.Add( Action.Property( on=target, property="Color",end=Vec4(1,1,1,1),duration=time))

Zero.RegisterComponent("Fader", Fader)