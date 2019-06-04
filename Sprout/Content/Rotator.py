import Zero
import Events
import Property
import VectorMath

import math

class Rotator:
    Disabled = Property.Bool(default = False)
    
    RotateX = Property.Bool( default = False )
    RotatorX = Property.Float( default = 0.0 )
    RotateY = Property.Bool( default = False )
    RotatorY = Property.Float( default = 0.0 )
    RotateZ = Property.Bool( default = False )
    RotatorZ = Property.Float( default = 0.0 )
    
    Sway = Property.Bool(default = False)
    SwayPeriod = Property.Float(default = 1.5)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        self.Timer = 0.0
        self.negator = 1.0
        self.StartingRotation = self.Owner.Transform.Rotation
    
    def onUpdate(self, Event):
        if self.Disabled:
            return
        
        NormalizedTime = Event.Dt * 0.5
        self.Timer += Event.Dt
        
        if self.Sway and self.Timer >= self.SwayPeriod:
            self.negator *= -1.0
            self.Timer = 0.0
        
        ##########################################
        ### The Following commented Code dictates how to rotate to certain points using methods that are most efficient to the Zero Engine
        #targetRotation = VectorMath.Quat.AxisAngle(VectorMath.Vec3(0,1,0), math.radians(50))
        
        #rot = VectorMath.Quat.RotateTowards(self.Owner.Transform.Rotation, targetRotation, math.radians(20) * Event.Dt)
        #self.Owner.Transform.Rotation = rot
        #########################################
        
        if self.RotateX:
            self.Owner.Transform.RotateByAnglesXYZ( self.negator * self.RotatorX * NormalizedTime, 0, 0 )
        
        if self.RotateY:
            self.Owner.Transform.RotateByAnglesXYZ( 0, self.negator * self.RotatorY * NormalizedTime, 0 )
        
        if self.RotateZ:
            self.Owner.Transform.RotateByAnglesXYZ( 0, 0, self.negator * self.RotatorZ * NormalizedTime )
    #enddef
    
    def Disable(self):
        self.Disabled = True
    
    def Enable(self):
        self.Disabled = False
    
    def resetRotation(self):
        self.Owner.Transform.Rotation = self.StartingRotation
#endclass

Zero.RegisterComponent("Rotator", Rotator)