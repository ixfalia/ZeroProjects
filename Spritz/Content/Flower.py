import Zero
import Events
import Property
import VectorMath

class Flower:
    DebugMode = Property.Bool(default = True)
    StartingShakeAmount =  Property.Float(default = 1.0)
    StartingShakeSpeed = Property.Float(default =  0.15)
    
    EndingShakeAmount = Property.Float(default = 2.0)
    EndingShakeSpeed = Property.Float(default = 0.45)
    
    def Initialize(self, initializer):
        if self.Owner.Rotator:
            self.Owner.Rotator.RotatorZ = self.StartingShakeAmount
            self.Owner.Rotator.SwayPeriod = self.StartingShakeSpeed
            if self.StartingShakeSpeed > 0:
                self.Owner.Rotator.Sway = True
        #endif
    #enddef
    
    

Zero.RegisterComponent("Flower", Flower)