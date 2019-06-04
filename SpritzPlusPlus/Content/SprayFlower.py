import Zero
import Events
import Property
import VectorMath

class SprayFlower:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.onCollisionEnd)
        
        self.Owner.Sprinkler.AutoSpray = False
    
    def onCollision(self, cEvent):
        other = cEvent.OtherObject
        
        if other.Player:
            self.Owner.Sprinkler.AutoSpray = True
    
    def onCollisionEnd(self, cEvent):
        other = cEvent.OtherObject
        
        if other.Player:
            self.Owner.Sprinkler.AutoSpray = False

Zero.RegisterComponent("SprayFlower", SprayFlower)