import Zero
import Events
import Property
import VectorMath

import math

Vec3 = VectorMath.Vec3

class Rotator:
    Active = Property.Bool( default = True )
    
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
        Zero.Connect(self.Owner, "ToggleRotation", self.onRotToggle)
        
        self.Timer = 0.0
        self.negator = 1.0
    
    def onUpdate(self, Event):
        if not self.Active:
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
            vecAxis = Vec3(1, 0, 0);
            angle = self.negator * self.RotatorX * math.pi * self.Timer;
            self.Owner.Transform.Rotation = VectorMath.Quat.AxisAngle(vecAxis, angle);
        
        if self.RotateY:
            vecAxis = Vec3(0, 1, 0);
            angle = self.negator * self.RotatorY * math.pi * self.Timer;
            self.Owner.Transform.Rotation = VectorMath.Quat.AxisAngle(vecAxis, angle);
        
        if self.RotateZ:
            vecAxis = Vec3(0, 0, 1);
            angle = self.negator * self.RotatorZ * math.pi * self.Timer;
            self.Owner.Transform.Rotation = VectorMath.Quat.AxisAngle(vecAxis, angle);
            #self.Owner.Transform.Translation = self.Owner.Transform.Rotation.rotate(Vec3(5, 0, 0))
    #enddef
    
    def onRotToggle(self, tEvent):
        self.Active = not self.Active
    
#endclass

Zero.RegisterComponent("Rotator", Rotator)