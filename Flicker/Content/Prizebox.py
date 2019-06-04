import Zero
import Events
import Property
import VectorMath
import random

Vec3 = VectorMath.Vec3

class Prizebox:
    DebugMode =  Property.Bool( default = True)
    PrizeType = Property.String("")
    VelocityY = Property.Float(default = 10)
    PrizeAmount = Property.Uint(default = 8)
    SoundCue = Property.String(default = "")
    EventType = Property.String(default = "")
    
    isUsed = Property.Bool( default = False )
    playSound = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "LockUnlocked", self.onLockEvent)
        
        if not self.EventType == "":
            print("Prizebox.Initialize() SpecialEvent Set to", self.EventType)
            Zero.Connect(self.Owner, self.EventType, self.onSpecialEvent)
    
    def prizeSplodeAny(self, prizeType, prizeAmount):
        if self.isUsed:
            return
            
        random.seed(self.Space.TimeSpace.CurrentTime)
        
        if not self.SoundCue == "":
            self.Owner.SoundEmitter.PlayCue(self.SoundCue)
        
        for i in range(self.PrizeAmount):
            collectible = self.Space.Create(prizeType)
            collectible.Transform.Translation = self.Owner.Transform.Translation + Vec3(0,0,0.01)
            collectible.RigidBody.Velocity = Vec3( 2*random.uniform(-1.0, 1.0), self.VelocityY, 0 )
            
        self.isUsed = True
    
    def prizeSplode(self):
        self.prizeSplodeAny(self.PrizeType, self.PrizeAmount)
        
        
    def onLockEvent(self, Event):
        if self.DebugMode:
            print("Prizebox in",self.Owner.Name, "received Unlock Message")
        self.prizeSplode()
    
    def onSpecialEvent(self, Event):
        if self.DebugMode:
            print("Prizebox in",self.Owner.Name, "received SpecialEvent Unlock")
        self.prizeSplode()

Zero.RegisterComponent("Prizebox", Prizebox)