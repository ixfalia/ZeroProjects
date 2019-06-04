import Zero
import Events
import Property
import VectorMath

import Action

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class Scalarator:
    Active = Property.Bool(default = False)
    Delay = Property.Float(default = 0.1)
    Duration = Property.Float(default = 0.5)
    ScaleX = Property.Float(default = 0)
    ScaleY = Property.Float(default = 0)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        self.startingScale = self.Owner.Transform.Scale
        self.seq = Action.Sequence(self.Owner)
        self.last = self.Active
        
        if self.Active:
            self.activate()
    
    def onUpdate(self, uEvent):
        if not self.last and self.Active:
            self.activate()
        #endif
        
        if self.last and not self.Active:
            self.seq.Cancel()
        
        self.last = self.Active
    
    def activate(self):
        self.Active = True
        
        target = self.Owner.Transform
        end = Vec3()
        
        if not self.ScaleX == 0:
            end.x = self.ScaleX
        elif not self.ScaleY == 0:
            end.y = self.ScaleY
        
        #print("Scalerator.activate(): End Scale is:", end)
        self.seq = Action.Sequence(self.Owner)
        
        Action.Property(self.seq, target, "Scale", end+self.startingScale, self.Duration, Action.Ease.Linear)
        Action.Delay(self.seq, self.Delay)
        Action.Property(self.seq, target, "Scale", self.startingScale, self.Duration, Action.Ease.Linear)
        Action.Call(self.seq, self.repeat)
        #raise
    
    def repeat(self):
        target = self.Owner.Transform
        end = Vec3()
        
        if not self.ScaleX == 0:
            end.x = self.ScaleX
        if not self.ScaleY == 0:
            end.y = self.ScaleY
        
        #print("Scalerator.activate(): End Scale is:", end)
        self.seq = Action.Sequence(self.Owner)
        
        Action.Property(self.seq, target, "Scale", end+self.startingScale, self.Duration, Action.Ease.Linear)
        Action.Delay(self.seq, self.Delay)
        Action.Property(self.seq, target, "Scale", self.startingScale, self.Duration, Action.Ease.Linear)
        Action.Call(self.seq, self.repeat)
    
    

Zero.RegisterComponent("Scalarator", Scalarator)
