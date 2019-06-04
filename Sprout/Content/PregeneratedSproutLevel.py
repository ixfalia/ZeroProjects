import Zero
import Events
import Property
import VectorMath

import myCustomEnums
sproutTypes = myCustomEnums.sproutTypes

class PregeneratedSproutLevel:
    LevelNumber = Property.Int(default = 0)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        
        self.MasterGrid = self.Space.FindObjectByName("MasterGrid")
        self.EffectManager = self.Space.FindObjectByName("LevelSettings").ManipulatorManager
        
        self.Levels = []
        self.registerLevels()
        pass
    
    def onLevel(self, lEvent):
        self.Levels[self.LevelNumber]()
        pass
    
    def registerLevels(self):
        self.Levels.append(self.Level1)
        self.Levels.append(self.Level2)
        self.Levels.append(self.Level3)
        self.Levels.append(self.Level4)
    
    def Level1(self):
        flowers = self.MasterGrid.FlowerGrid
        self.EffectManager.changeSpawnTable("OnlyBlue")
        #print(table)
        
        seed = flowers.placeSeed(3,3,sproutTypes.blue)
        #seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(3,4,sproutTypes.blue)
        #seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(4,3,sproutTypes.blue)
        #seed.Sprout.bloomFlower()
    
    def Level2(self):
        flowers = self.MasterGrid.FlowerGrid
        self.EffectManager.changeSpawnTable("OnlyBlue")
        self.EffectManager.Owner.TurnManager.changeTurnCount(5)
        #print(table)
        
        seed = flowers.placeSeed(0,4,sproutTypes.blue)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(1,4,sproutTypes.blue)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(2,5,sproutTypes.blue)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(2,6,sproutTypes.blue)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(3,4,sproutTypes.blue)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(4,4,sproutTypes.blue)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(2,3,sproutTypes.blue)
        seed = flowers.placeSeed(2,2,sproutTypes.blue)
        #seed.Sprout.onBloom(None)
    
    def Level3(self):
        flowers = self.MasterGrid.FlowerGrid
        self.EffectManager.changeSpawnTable("OnlyColors")
        self.EffectManager.Owner.TurnManager.changeTurnCount(16)
        
        seed = flowers.placeSeed(1,5,sproutTypes.poison)
        #seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(1,1,sproutTypes.poison)
        #seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(5,1,sproutTypes.poison)
        #seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(5,5,sproutTypes.poison)
    
    def Level4(self):
        flowers = self.MasterGrid.FlowerGrid
        self.EffectManager.changeSpawnTable("Tutorial4")
        self.EffectManager.Owner.TurnManager.changeTurnCount(12)
        
        
        return
        seed = flowers.placeSeed(1,3,sproutTypes.blue)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(1,4,sproutTypes.blue)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(1,6,sproutTypes.blue)
        seed.Sprout.bloomFlower()
        
        seed = flowers.placeSeed(3,3,sproutTypes.red)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(3,4,sproutTypes.red)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(3,6,sproutTypes.red)
        seed.Sprout.bloomFlower()
        
        seed = flowers.placeSeed(2,3,sproutTypes.yellow)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(2,4,sproutTypes.yellow)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(2,6,sproutTypes.yellow)
        seed.Sprout.bloomFlower()
        
        seed = flowers.placeSeed(4,3,sproutTypes.weed)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(4,4,sproutTypes.weed)
        seed.Sprout.bloomFlower()
        seed = flowers.placeSeed(4,6,sproutTypes.weed)
        seed.Sprout.bloomFlower()
    
Zero.RegisterComponent("PregeneratedSproutLevel", PregeneratedSproutLevel)