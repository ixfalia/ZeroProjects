import Zero
import Events
import Property
import VectorMath

class SpritzFlower:
    isUsed = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        #print("spritzfloawer")
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.onCollision)
        #Zero.Connect(self.Owner, "WaterEvent", self.onWater)
        
        if self.isUsed:
            Activated = Zero.ScriptEvent()
            
            self.Owner.DispatchEvent("ActivateEvent", Activated)
        
    def onCollision(self, Event):
        other = Event.OtherObject
        #print("colliding")
        if other.Water:
            #print("other.water")
            self.Owner.Prizebox.prizeSplode()
            #self.Owner.Sprite.Color =  VectorMath.Vec4(0,0.6,0.7,1)
            
            Activated = Zero.ScriptEvent()
            
            self.Owner.DispatchEvent("ActivateEvent", Activated)
            
            if not self.isUsed:
                self.Owner.SoundEmitter.Play()
            
            self.isUsed = True
    
    def onWater(self, Event):
        #print("colliding")
        self.Owner.Prizebox.prizeSplode()

Zero.RegisterComponent("SpritzFlower", SpritzFlower)