import Zero
import Events
import Property
import VectorMath

class SoundManager:
    DebugMode = Property.Bool(default = True)
    MaxSoundLimit = Property.Int(default = 50)
    SoundLimit =  Property.Float(default = 0.5) #Determines how often sounds can be played
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        self.SoundTimer = 0.0
        self.SoundsPlayable = False
    
    def onUpdate(self, UpdateEvent):
        self.SoundTimer += UpdateEvent.Dt
        
        if self.SoundTimer > self.SoundLimit:
            self.SoundsPlayable = True
            self.SoundTimer = 0.0
    
    def Play(self, SoundCue):
        
        if self.DebugMode:
            print( "SoundManager.Play: Sound Cue: ", SoundCue)
        
        if not SoundCue == "Spray":
            self.Owner.SoundEmitter.PlayCue(SoundCue)
            self.SoundsPlayable = False
            self.SoundTimer = 0.0
        elif self.SoundsPlayable and self.Owner.WaterTank.isNotEmpty():
            self.Owner.SoundEmitter.PlayCue(SoundCue)
            self.SoundsPlayable = False
            self.SoundTimer = 0.0

Zero.RegisterComponent("SoundManager", SoundManager)