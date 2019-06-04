import Zero
import Events
import Property
import VectorMath

class Spikey:
    FaceSprite = Property.SpriteSource()
    AngrySprite = Property.SpriteSource()
    WaterPauseTime = Property.Float(default = 1.5)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        
        self.WaterPauseTimer = 0
        self.Owner.PathFollower.Paused = False
        self.delayed = False
        self.initialSway = self.Owner.Rotator.SwayPeriod
    
    def onUpdate(self, uEvent):
        self.WaterPauseTimer += uEvent.Dt
        
        if self.WaterPauseTimer >= self.WaterPauseTime:
            self.delayed = False
            self.Owner.PathFollower.Paused = False
            self.Owner.PutAnotherSprite.CreateNewSprite(self.FaceSprite)
            #self.Owner.Rotator.Sway = False
            #self.Owner.Rotator.SwayPeriod = self.initialSway
    #end onUpdate()
    
    def onCollision(self, cEvent):
        other = cEvent.OtherObject
        
        if other.Water and not self.delayed:
            self.delayed = True
            self.WaterPauseTimer = 0
            self.Owner.PathFollower.Paused = True
            #self.Owner.Rotator.SwayPeriod = 0.2
            #self.Owner.Rotator.Sway = True
            
            self.Owner.PutAnotherSprite.CreateNewSprite(self.AngrySprite)

Zero.RegisterComponent("Spikey", Spikey)