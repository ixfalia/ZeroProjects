import Zero
import Events
import Property
import VectorMath

class Fountain:
    Timer = 0
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.update)
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.persist)
        
    
    def update(self, Event):
        #print("update")
        self.Timer += Event.Dt
        
    def persist(self, Event):
        #print("fountain hit")
        other = Event.GetOtherObject(self.Owner)
        if other.PlayerController:
            other.WaterTank.replenish(0.005)
            if self.Timer >= 0.55:
                #print("playing sound")
                self.Owner.SoundEmitter.Play()
                self.Timer = 0


Zero.RegisterComponent("Fountain", Fountain)