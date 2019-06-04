import Zero
import Events
import Property
import VectorMath

class Beacon:
    isActive = Property.Bool(default = True)
    HealRate = Property.Float(default = 2)
    Timer = 0
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "HealthEvent", self.onHealth)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
    
    
    def onUpdate(self, Event):
        self.Timer += Event.Dt
        
        if self.Timer >= self.HealRate:
            #print("heal")
            #self.Owner.Health.healDamage(1)
            #self.updateColor()
            self.Timer = 0
            
    
    def onCollision(self, Event):
        other = Event.GetOtherObject(self.Owner)
        
        if other.Health:
            self.updateColor()
    
    def onHealth(self, Event):
        if Event.CurrentHealth <= 0:
            self.Owner.SpriteParticleSystem.Clear()
            self.Owner.SphericalParticleEmitter.Active = False
            self.Owner.Model.Material =  "Black"
            
            self.isActive = False
        
    def updateColor(self):
        if self.isActive == False:
            self.Owner.Model.Material =  "Black"
            return
        
        old = self.Owner.SpriteParticleSystem.Tint
        self.Owner.SpriteParticleSystem.Tint = VectorMath.Vec4(1*1-self.Owner.Health.normalizedHealth(), old.y*0.5, old.z*0.5, 1)
        
        if self.Owner.Model.Material == "Black":
            self.Owner.Model.Material = "Black"
        elif self.Owner.Health.normalizedHealth() < 0.4:
            self.Owner.Model.Material = "Red"
        elif self.Owner.Health.normalizedHealth() > 0.4:
            self.Owner.Model.Material = "BeaconGlow"

Zero.RegisterComponent("Beacon", Beacon)