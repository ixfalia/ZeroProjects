import Zero
import Events
import Property
import VectorMath

import math
Vec3 = VectorMath.Vec3

class Orbit:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Active = Property.Bool(default = True)
        self.OrbitCog = Property.Bool(default = True)
        
        self.TargetPlayer = Property.Bool(default = False)
        self.Target = Property.Cog()
        self.PointTarget = Property.Vector3()
        
        self.Radius = Property.Float()
        self.Rate = Property.Float()
        
        self.RotateX = Property.Bool(default = False)
        self.RotateY = Property.Bool(default = False)
        self.RotateZ = Property.Bool(default = False)
        
        self.Sway = Property.Bool(default = False)
        pass

    def Initialize(self, initializer):
        self.Timer = 0
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        pass

    def onUpdate(self, Event):
        if not self.Active:
            return
        
        if self.TargetPlayer:
            target = self.getPlayer().Transform.Translation
        elif self.Target:
            target = self.Target.Transform.Translation
        elif self.PointTarget:
            target = self.PointTarget
        else:
            target = None
            raise
        
        if not target:
            return
        
        NormalizedTime = Event.Dt * 0.5
        self.Timer += Event.Dt
        
        if self.Sway and self.Timer >= self.SwayPeriod:
            self.negator *= -1.0
            self.Timer = 0.0
        
        trans =  self.Owner.Transform.Translation
        
        ##########################################
        ### The Following commented Code dictates how to rotate to certain points using methods that are most efficient to the Zero Engine
        #targetRotation = VectorMath.Quat.AxisAngle(VectorMath.Vec3(0,1,0), math.radians(50))
        
        #rot = VectorMath.Quat.RotateTowards(self.Owner.Transform.Rotation, targetRotation, math.radians(20) * Event.Dt)
        #self.Owner.Transform.Rotation = rot
        #########################################
        
        vecAxis = Vec3(0, 0, 1);
        angle = self.Rate * math.pi * self.Timer;
        
        rot = VectorMath.Quat.EulerXYZ(0, 1 * Event.Dt, 0)
        self.Owner.Transform.Translation = self.RotatePointAroundPivot(trans, target, rot)
        #print(self.Owner.Transform.Translation)
    #enddef
    
    def changeTarget(self, Target):
        pass
    
    def getPlayer(self):
        return self.GameSession.PlayerTracker.getPlayer()
    
    def RotatePointAroundPivot(self, point, pivot, angle):
        return angle.rotate((point - pivot) + pivot)
    
    def distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

Zero.RegisterComponent("Orbit", Orbit)