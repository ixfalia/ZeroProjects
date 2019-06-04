import Zero
import Events
import Property
import VectorMath

class SoundManage:
    Debug = Property.Bool(default = False)
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "PlaySoundEvent", self.onPlaySound)
    
    def onPlaySound(self, sEvent):
        if self.Debug:
            print("SoundManage.onPlaySound(): Sound Recieved")
            print("\tPlaying Sound: ", sEvent.Sound)
        if not sEvent.Pitch:
            pitch = 1
        else:
            pitch = sEvent.Pitch
        if not sEvent.Volume:
            volume = 1
        else:
            volume = sEvent.Volume
        
        if sEvent.Sound == "LevelEnd":
            self.Owner.SoundEmitter.Pitch = 1
            self.Owner.SoundEmitter.PlayCue(sEvent.Sound)
            return
        
        self.Owner.SoundEmitter.Pitch = pitch
        self.Owner.SoundEmitter.PlayCue(sEvent.Sound)
        #raise

Zero.RegisterComponent("SoundManage", SoundManage)