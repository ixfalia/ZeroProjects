import Zero
import Events
import Property
import VectorMath
import random

Vec3 = VectorMath.Vec3

class Prizebox:
    DebugMode =  Property.Bool( default = True)
    PrizeType = Property.String("twinkle")
    VelocityY = Property.Float(default = 10)
    PrizeAmount = Property.Uint(default = 8)
    SoundCue = Property.SoundCue()
    
    isUsed = Property.Bool( default = False )
    playSound = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "LockUnlocked", self.onLockEvent)
        
        self.Owner.Transform.Translation.z -= 0.9
    
    def prizeSplodeAny(self, prizeType, prizeAmount):
        if self.isUsed:
            return
            
        random.seed(self.Space.TimeSpace.CurrentTime)
        
        if not self.SoundCue == "":
            self.Owner.SoundEmitter.Pitch = 1
            self.Owner.SoundEmitter.PlayCue(self.SoundCue)
        
        for i in range(self.PrizeAmount):
            collectible = self.Space.Create(prizeType)
            collectible.Transform.Translation = self.Owner.Transform.Translation + Vec3(0,0,0.01)
            collectible.Transform.Translation *= Vec3(1,1,0.1)
            collectible.RigidBody.Velocity = Vec3( 2*random.uniform(-1.0, 1.0), self.VelocityY, 0 )
            
        self.isUsed = True
    
    def prizeSplode(self):
        self.prizeSplodeAny(self.PrizeType, self.PrizeAmount)
        
        
    def onLockEvent(self, Event):
        if self.DebugMode:
            print("Prizebox in",self.Owner.Name, "received Unlock Message")
        self.prizeSplode()

Zero.RegisterComponent("Prizebox", Prizebox)