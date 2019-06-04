import Zero
import Events
import Property
import VectorMath

class Health:
    DebugMode = Property.Bool(default = False)
    MaxHealth = Property.Float(default = 100)
    CurrentHealth = Property.Float(default = 100)
    
    hasDamageReduction = Property.Bool(default = False)
    DamageReduction = Property.Float(default = 10)
    
    def Initialize(self, initializer):
        self.CurrentHealth = self.MaxHealth
    
    def takeDamage(self, damage = 25):
        if self.hasDamageReduction:
            damage = damage - self.DamageReduction
            
            if damage < 0:
                damage = 0
        #endif
        
        self.CurrentHealth -= damage
        
        if self.DebugMode:
            print(self.Owner.Name, "Health.takeDamage(): Took", damage, "Damage. CurrentHealth", self.CurrentHealth)
        if self.CurrentHealth <= 0:
            self.CurrentHealth = 0
            
            HealthEvent = Zero.ScriptEvent()
            HealthEvent.CurrentHealth = self.CurrentHealth
            HealthEvent.MaxHealth =  self.MaxHealth
            HealthEvent.Who = self.Owner
            self.Owner.DispatchEvent("HealthEvent",HealthEvent)
        #endif
        
        if self.Owner.PlayerController:
            self.Owner.SoundEmitter.PlayCue("Hit")
    #enddef
    
    def healDamage(self, heal = 30):
        self.CurrentHealth += heal
        
        if self.CurrentHealth > self.MaxHealth:
            self.CurrentHealth = self.MaxHealth
            
        HealthEvent = Zero.ScriptEvent()
        HealthEvent.CurrentHealth = self.CurrentHealth
        HealthEvent.MaxHealth =  self.MaxHealth
        HealthEvent.Who = self.Owner
        self.Owner.DispatchEvent("HealthEvent",HealthEvent)
    
    def normalizedHealth(self):
        return float(self.CurrentHealth / self.MaxHealth)
    
    def percentHealth(self):
        return 100 * float(self.CurrentHealth / self.MaxHealth)

Zero.RegisterComponent("Health", Health)