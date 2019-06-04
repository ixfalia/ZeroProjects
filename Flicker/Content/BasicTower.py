import Zero
import Events
import Property
import VectorMath

class BasicTower:
    DebugMode = Property.Bool(default = True)
    
    Range = Property.Float(default = 256)
    TurnSpeed = Property.Float(default = 1.0)
    AttackSpeed = Property.Float(default = 3 )
    
    def Initialize(self, initializer):
        Timer.registerTimer("TowerAttack", self.AttackSpeed, self.AimAndShoot, True)
        
    
    def AimAndShoot(self):
        pass
    
    def Aim(self):
        pass
    
    def Shoot(self):
        pass
    
#end class BasicTower

Zero.RegisterComponent("BasicTower", BasicTower)