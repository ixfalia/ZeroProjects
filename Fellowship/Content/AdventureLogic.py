import Zero
import Events
import Property
import VectorMath

import random

class AdventureLogic:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.MaxDiceBonus = Property.Uint(default = 10)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        pass
    
    def DepleteStaminaCalculated(self, amount, successBy = 1):
        variation = 0.2 * (1/(1 + successBy))
        deplete = random.Random() * variation
        
        self.DepleteStats(deplete)
    
    def DepleteStats(self, stat, amount):
        self.GameSession.Statistics.addStat(stat, -amount)
        pass
    
    def IncremenetTime(self, amount):
        pass
    
    def TakeDamage(self, amount):
        pass
    
    def StatCheck(self, stat):
        statValue = self.GameSession.Statistics.getStat(stat)
        statMod = self.StatToMod(statValue)
        
        result = self.Roll3D6Mod(statMod)
        
        return result
    
    def StatToMod(self, stat):
        returner =  stat * self.MaxDiceBonus
        
        return returner
    
    def Roll3D6Mod(self, mod):
        return self.Roll3D6() + mod
    
    def Roll3D6(self):
        return self.RollD6(amount)
    
    def RollD6Mod(self, amount, mod):
        return self.RollD6(amount) + mod

    def RollD6(self, amount = 1):
        returner = 0
        
        for i in range(amount):
            returner += random.randint(1, 6)
        
        return returner
    
    def RollDX(self, sides, times):
        returner = 0
        
        for i in range(amount):
            returner += random.randint(1, sides)
        
        return returner

Zero.RegisterComponent("AdventureLogic", AdventureLogic)