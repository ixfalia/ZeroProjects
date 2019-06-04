import Zero
import Events
import Property
import VectorMath

import Color
import random
import colorsys

import EnumDeclarations
Types = EnumDeclarations.Types
TColor = EnumDeclarations.TypeToColor

class Food:
    def DefineProperties(self):
        self.RandomColor = Property.Bool(default = False)
        self.RandomBerry = Property.Bool(default = False)
        
        self.HealthMod = Property.Uint(default = 0)
        self.FullnessMod = Property.Float(default = 0.25)
        
        self.PhysicalMod = Property.Float()
        self.SpecialMod = Property.Float()
        self.DefenseMod = Property.Float()
        self.ResistanceMod = Property.Float()
        self.SpeedMod = Property.Float()
        
        self.HappinessMod = Property.Float(default = 0.1)
        
        self.MaxHealthMod = Property.Float()
        self.MaxStaminaMod = Property.Float()
        self.Satiation = Property.Float()
        
        self.Type = Property.Enum("Types")
        self.TypeStrength = Property.Float(default = 0.25)
        
        self.TimeToEat = Property.Float(default = 2)
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        if self.RandomColor:
            self.Color = self.getRandomColor()
            self.Owner.Sprite.Color = self.Color
        else:
            self.Color = self.Owner.Sprite.Color
        
        if self.RandomBerry:
            self.randomizeStats()
        
        self.Eaten = False
        pass
    
    def getRandomColor(self):
        owner = self.Owner.Sprite.Color
        
        color = colorsys.rgb_to_hsv(owner.r, owner.g, owner.b)
        nuColor = colorsys.hsv_to_rgb(random.random(), color[1], color[2])
        
        returner = VectorMath.Vector4(nuColor[0], nuColor[1], nuColor[2], 1)
        
        return returner

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def randomizeStats(self):
        statMods = ["Physical", "Special", "Defense", "Resistance", "Speed"]
        
        for i in range(3):
            stat = random.choice(statMods)
            
            if self.__dict__["{}Mod".format(stat)] <= 0.01:
                self.__dict__["{}Mod".format(stat)] = random.random()
        
        #self.PhysicalMod = random.random()
        #self.SpecialMod = random.random()
        #self.DefenseMod = random.random()
        #self.ResistanceMod = random.random()
        #self.SpeedMod = random.random()
        #self.MaxHealthMod = random.random()
        #self.MaxStaminaMod = random.random()
        
        self.Type = random.choice(EnumDeclarations.TypeList)
        self.TypeStrength = random.random()
        
        self.Color = EnumDeclarations.TypeToColor[self.Type]
        
        self.Owner.Sprite.Color = self.Color
    
    def setStat(self, stat, value):
        self.__dict__[stat] = value
    
    def ApplyFood(self, target):
        target = self.GameSession
        #print(self.__dict__)
        #raise
        #target.Statistics.addStat("Health", self.HealthMod)
        target.Statistics.addStat("Physical", self.PhysicalMod)
        target.Statistics.addStat("Special", self.SpecialMod)
        target.Statistics.addStat("Defense", self.DefenseMod)
        target.Statistics.addStat("Resistance", self.ResistanceMod)
        target.Statistics.addStat("Speed", self.SpeedMod)
        
        #target.Statistics.addStat("MaxHealth", self.MaxHealthMod)
        #target.Statistics.addStat("MaxStamina", self.MaxStaminaMod)
        
        target.Statistics.addStat("Health", self.HealthMod)
        target.Statistics.addStat("Hunger", self.FullnessMod)
        target.Statistics.addStat("Fullness", self.FullnessMod)
        
        target.Statistics.addStat("Happiness", self.HappinessMod)
        
        target.Statistics.addStat("Energy", -0.1)
        
        target.Statistics.finishedAdding()
        
        target.Statistics.Pet.Sprite.Color.lerp(self.Color, self.FullnessMod)
        self.Eaten = True
    
    def oldApplyFood(self, target):
        target.Statistics.Health += self.HealthMod
        
        target.Statistics.Physical += self.PhysicalMod
        target.Statistics.Special += self.SpecialMod
        target.Statistics.Defense += self.DefenseMod
        target.Statistics.Resistance += self.ResistanceMod
        target.Statistics.Speed += self.SpeedMod
        
        target.Statistics.MaxHealth += self.MaxHealthMod
        target.Statistics.MaxStamina += self.MaxStaminaMod
        
        target.Statistics.Hunger += self.FullnessMod
        target.Statistics.Fullness += self.FullnessMod
        
        target.Sprite.Color.lerp(self.Color, self.FullnessMod)
        
        self.Eaten = True

Zero.RegisterComponent("Food", Food)