import Zero
import Events
import Property
import VectorMath

class SoundActivator:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, "SoundEvent", self.onSound)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onSound(self, sEvent):
        cue = sEvent.Cue
        self.play(cue)
    
    def play(self, cue):
        self.Owner.SoundEmitter.PlayCue(cue)

Zero.RegisterComponent("SoundActivator", SoundActivator)