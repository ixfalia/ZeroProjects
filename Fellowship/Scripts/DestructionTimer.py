import Zero
import Events
import Property
import VectorMath

import Action

class DestructionTimer:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Active = Property.Bool(default = True)
        self.Duration = Property.Float(1.0)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        if not self.Active:
            return
        
        self.activate()
        pass
    
    def activate(self):
        self.Active = True
        
        self.seq = Action.Sequence(self.Owner)
        Action.Delay(self.seq, self.Duration)
        Action.Call(self.seq, self.destruction)

    def destruction(self):
        duration = 0
        
        if self.Owner.SphericalParticleEmitter:
            emitter = self.Owner.SphericalParticleEmitter
            duration += emitter.Lifetime + emitter.LifetimeVariance
            
            emitter.Active = False
            
            print(self.Owner.SphericalParticleEmitter.Active)
            raise
        
        Action.Delay(self.seq, duration)
        Action.Call(self.seq, self.Owner.Destroy)

Zero.RegisterComponent("DestructionTimer", DestructionTimer)