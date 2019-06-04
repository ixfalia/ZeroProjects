import Zero
import Events
import Property
import VectorMath

class HealthPoints:
    HealthMax = Property.Int(default = 3)
    CurrentHealth = Property.Int(default = 2)
    
    def Initialize(self, initializer):
        self.DefaultHealth = self.CurrentHealth
        pass
    
    def takeDamage(self, damage = 1):
        self.addHealth(-damage)
    
    def healDamage(self, heal = 1):
        self.addHealth(heal)
    
    def addHealth(self, amount):
        self.CurrentHealth += amount
        hEvent = Zero.ScriptEvent()
        
        if self.CurrentHealth >= self.HealthMax:
            self.CurrentHealth = self.HealthMax
            hEvent.Health = self.CurrentHealth
            self.Owner.DispatchEvent("FullHealth", hEvent)
            
        elif self.CurrentHealth <= 0:
            self.CurrentHealth = 0
            hEvent.Health = self.CurrentHealth
            self.Owner.DispatchEvent("DeathEvent", hEvent)
    
    def getHealthPercent(self):
        return (self.CurrentHealth/self.HealthMax)*100
    
    def getHealthNormalized(self):
        return self.CurrentHealth/self.HealthMax
    
    def reset(self):
        self.CurrentHealth = self.DefaultHealth

Zero.RegisterComponent("HealthPoints", HealthPoints)