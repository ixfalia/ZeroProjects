import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class Scalerator:
    DebugMode = Property.Bool(default = True)
    ScaleX = Property.Bool( default = False )
    ScaleratorX = Property.Float( default = 0.0 )
    ScaleY = Property.Bool( default = False )
    ScaleratorY = Property.Float( default = 0.0 )
    ScaleZ = Property.Bool( default = False )
    ScaleratorZ = Property.Float( default = 0.0 )
    
    Breathe = Property.Bool( default = False )
    BreatheRate = Property.Float(default = 1.5)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        self.Timer = 0.0
        self.negator = 1.0
        self.ScaleOld = self.Owner.Transform.Scale.x
    
    def onUpdate(self, Event):
        NormalizedTime = Event.Dt * 0.5
        self.Timer += Event.Dt
        
        if self.DebugMode:
            print( "ScaleOld: ", self.ScaleOld, "Current Scale:", self.Owner.Transform.Scale, "Timer: ", self.Timer)
        
        if self.Breathe and self.Timer >= self.BreatheRate:
            self.negator *= -1.0
            self.Timer = 0.0
        
        if self.ScaleX:
            self.Owner.Transform.Scale = Vec3( self.negator * self.ScaleratorX * NormalizedTime, self.ScaleOld, self.ScaleOld )
        
        if self.ScaleY:
            self.Owner.Transform.Scale = Vec3( self.ScaleOld, self.negator * self.ScaleratorY * NormalizedTime, self.ScaleOld )
        
        if self.ScaleZ:
            self.Owner.Transform.Scale = Vec3( self.ScaleOld, self.ScaleOld, self.negator * self.ScaleratorZ * NormalizedTime )
    #enddef

Zero.RegisterComponent("Scalerator", Scalerator)