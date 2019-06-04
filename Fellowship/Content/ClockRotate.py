import Zero
import Events
import Property
import VectorMath

import Action
import math

class ClockRotate:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.TickTime = Property.Float(default = -1)
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, "PetRegisterEvent", self.onPet)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        
        self.Timer = 0
        pass
    
    def resetTimer(self):
        axis = VectorMath.Vec3(0, 0, 1)
        angle = (361 * math.pi) / 180
        rot = VectorMath.Quat.AxisAngle(axis, angle)
        microRot = VectorMath.Quat.AxisAngle(axis, angle * 2)
        
        #self.Owner.Transform.Rotation = rot
        
        seq = Action.Sequence(self.Owner)
        Action.Property(seq, self.Owner.Transform, "Rotation", rot, self.TickTime)
        #Action.Property(seq, self.Owner.Transform, "Rotation", microRot, self.TickTime / 2)
        #Action.Call(seq, self.resetRotation)
        Action.Call(seq, self.resetTimer)
    
    def resetRotation(self):
        axis = VectorMath.Vec3(0, 0, 1)
        angle = (0 * math.pi) / 180
        rot = VectorMath.Quat.AxisAngle(axis, angle)
        
        self.Owner.Transform.Rotation = rot

    def OnLogicUpdate(self, UpdateEvent):
        self.Timer += UpdateEvent.Dt
        
        axis = VectorMath.Vec3(0, 0, 1)
        oangle = (1 * math.pi) / 180
        rot = VectorMath.Quat.AxisAngle(axis, oangle * UpdateEvent.Dt)
        
        vecAxis = VectorMath.Vec3(0, 0, 1);
        angle = 2 * math.pi * (self.Timer/(self.TickTime -1))
        self.Owner.Transform.Rotation = VectorMath.Quat.AxisAngle(vecAxis, -angle);
        
        if self.Timer > self.TickTime - 1:
            self.Timer = 0
        #self.
        pass
    
    def onLevel(self, LevelEvent):
        #self.resetTimer()
        pass
    
    def onPet(self, PetEvent):
        pet = PetEvent.Sender
        
        if self.TickTime < 0:
            self.TickTime = pet.PetLogic.TickTime

Zero.RegisterComponent("ClockRotate", ClockRotate)