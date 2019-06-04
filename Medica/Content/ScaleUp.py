import Zero
import Events
import Property
import VectorMath

import Action

Vec2 = VectorMath.Vec2
Vec3 = VectorMath.Vec3

class ScaleUp:
    Active = Property.Bool(default = True)
    UniformScale = Property.Float(default = 0)
    ScaleX = Property.Float(default = 0)
    ScaleY = Property.Float(default = 0)
    Duration = Property.Float(default = 1)
    
    def Initialize(self, initializer):
        self.StartingScale = self.Owner.Transform.Scale
        
        if self.UniformScale == 0.0:
            self.Scaler = Vec2(self.ScaleX, self.ScaleY)
        else:
            self.Scaler = Vec2(self.UniformScale, self.UniformScale)
        
        self.seq = Action.Group(self.Owner)
        
        if self.Active:
            self.activate()
    
    def activate(self, duration = None):
        if not duration:
            duration = self.Duration
            
        self.seq = Action.Group(self.Owner)
        self.Active = True
        
        scalePrime = self.StartingScale + self.Scaler
        #print(self.StartingScale, self.Scaler, scalePrime)
        Action.Property(self.seq, self.Owner.Transform, "Scale", scalePrime, duration)
    
    def revert(self, duration = None):
        if not duration:
            duration = self.Duration
        
        if self.Active:
            Action.Property(self.seq, self.Owner.Transform, "Scale", self.StartingScale, duration)
    
    def deactivate(self):
        Action.Cancel(self.seq)
        
        self.Active = False

Zero.RegisterComponent("ScaleUp", ScaleUp)