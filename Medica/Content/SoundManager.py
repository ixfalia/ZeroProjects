import Zero
import Events
import Property
import VectorMath

class SoundManager:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "ChangeBGM", self.onChangeBGM)
        Zero.Connect(self.Space, "PlaySound", self.onPlaySound)
    
    def changeBGM(self, music):
        self.Owner.SoundEmitter.Stop()
        self.Owner.SoundEmitter.PlayCue(music)
    
    def playEffect(self, sound):
        eP = self.Space.FindObjectByName("effectPlayer")
        eP.SoundEmitter.PlayCue(sound)
    
    def onChangeBGM(self, e):
        self.changeBGM(e.Name)
    
    def onPlaySound(self, e):
        self.playEffect(e.Name)

Zero.RegisterComponent("SoundManager", SoundManager)