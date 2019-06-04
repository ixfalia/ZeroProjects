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
        
        self.ListenFor = Property.String()
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        #if not self.Active:
        #    return
        
        if not self.ListenFor == "":
            Zero.Connect(self.Space, self.ListenFor, self.onEvent)
        
        self.seq = Action.Sequence(self.Owner)
        if self.Active:
            self.activate()
        pass
    
    def activate(self):
        self.Active = True
        
        if not self.seq:
            self.seq = Action.Sequence(self.Owner)
        
        Action.Delay(self.seq, self.Duration)
        Action.Call(self.seq, self.destruction)
    
    def deactivate(self):
        self.Active = False
        if not self.seq:
            self.seq = Action.Sequence(self.Owner)
        
        self.seq.Cancel()

    def destruction(self):
        duration = 0
        
        if self.Owner.SphericalParticleEmitter:
            emitter = self.Owner.SphericalParticleEmitter
            duration += emitter.Lifetime + emitter.LifetimeVariance
            
            emitter.Active = False
            
            #print(self.Owner.SphericalParticleEmitter.Active)
        
        Action.Delay(self.seq, duration)
        Action.Call(self.seq, self.Owner.Destroy)
    
    def onEvent(self, Event):
        self.Owner.Destroy()
        Zero.Disconnect(self.Space, self.ListenFor, self.onEvent)

Zero.RegisterComponent("DestructionTimer", DestructionTimer)