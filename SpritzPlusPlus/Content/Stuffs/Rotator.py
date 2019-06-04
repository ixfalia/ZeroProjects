import Zero
import Events
import Property
import VectorMath

class Rotator:
    RotateX = Property.Bool( default = False )
    RotatorX = Property.Float( default = 0.0 )
    RotateY = Property.Bool( default = False )
    RotatorY = Property.Float( default = 0.0 )
    RotateZ = Property.Bool( default = False )
    RotatorZ = Property.Float( default = 0.0 )
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
    
    def onUpdate(self, Event):
        NormalizedTime = Event.Dt * 0.5
        
        if self.RotateX:
            self.Owner.Transform.RotateByAnglesXYZ( self.RotatorX * NormalizedTime, 0, 0 )
        
        if self.RotateY:
            self.Owner.Transform.RotateByAnglesXYZ( 0, self.RotatorY * NormalizedTime, 0 )
        
        if self.RotateZ:
            self.Owner.Transform.RotateByAnglesXYZ( 0, 0, self.RotatorZ * NormalizedTime )
    #enddef
#endclass

Zero.RegisterComponent("Rotator", Rotator)