import Zero
import Events
import Property
import VectorMath

import string

class AccomplishmentDataManager:
    class LevelData:
        HighScore = int(0)
        Deaths = int(0)
        Flowers = int(0)
        TotalFlowers = int(0)
        BestTime = 0.0
        
        def __init__(self, Level, LName, TotalFlowers):
            self.Level = Level
            self.LevelName = LName
            self.TotalFlowers = TotalFlowers
            self.Played = False
            self.Completed = False
        #end __init__()
    #endclass
    
    #HighestScore = Property.Uint(default = 0)
    PointsTotal = Property.Uint(default = 0)
    TotalDeaths = Property.Uint(default = 0)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "FlowerEvent", self.onFlowerGet)
        Zero.Connect(self.Owner, "PointsEvent", self.onPoints)
        Zero.Connect(self.Owner, "LevelEnd", self.onLevelComplete)
        #Zero.Connect(self.Owner, "DeathEvent", self.onDeath)
        
        self.TotalLevels = self.Owner.LevelManager.getLevelCount()#Zero.Game.LevelManager.getLevelCount()
        self.Data = []
        self.TotalFlowers = [0,0,0,5,6,0]
        
        for i in range(self.TotalLevels):
            flowers = self.Owner.LevelManager.levelTable.GetWeightAt(i)
            if int(flowers) > 1:
                flowers = int(flowers)
                #print(flowers)
            else:
                flowers = 0
            name = self.Owner.LevelManager.levelTable.GetNameAt(i)
            thingy = self.LevelData(self.Owner.LevelManager.getLevel(i), name, int(flowers))
            self.Data.insert(i, thingy)
        
        self.printData()
    
    def readFileData(self):
        pass
    
    def getLevelData(self, index):
        returner = self.Data[index]
        
        return returner
    
    def printData(self):
        print("\tCurrentLevel Data:")
        
        for info in self.Data:
            print("\tLevel Name:", info.LevelName)
            print("\t\tFlowersCollected: {0} / {1}".format(info.Flowers, info.TotalFlowers))
            print("\t\tHighScore: ", info.HighScore)
            print("\t\tBest Time: ", info.BestTime)
    
    def onFlowerGet(self, fEvent):
        currentID = self.Owner.LevelManager.getCurrentLevelIndex()
        flowers = self.Data[currentID].Flowers
        levelFlowers = fEvent.FlowerCount
        
        print(Zero.Game.LevelManager.levelTable.GetResourceAt(currentID).Name)
        print(flowers)
        print(levelFlowers)
        
        if levelFlowers > flowers:
            self.Data[currentID].Flowers = fEvent.FlowerCount
    
    def onPoints(self, pEvent):
        currentID = self.Owner.LevelManager.getCurrentLevelIndex()
        score = self.Data[currentID].HighScore
        
        #self.printData()
        #print(self.Owner.LevelManager.levelTable.GetResourceAt(currentID).Name)
        #print(score)
        #print(pEvent.Points)
        
        if score < pEvent.Points:
            self.Data[currentID].HighScore = pEvent.Points
    
    def onLevelComplete(self, lEvent):
        self.Data[currentID].Played = True
    
    def checkIfPlayed(self, Level):
        ID = Zero.Game.LevelManager.levelTable.FindIndexOfResource(Level)
        return self.Data[ID].Played

Zero.RegisterComponent("AccomplishmentDataManager", AccomplishmentDataManager)