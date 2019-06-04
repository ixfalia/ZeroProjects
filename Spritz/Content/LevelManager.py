import Zero
import Events
import Property
import VectorMath

class LevelManager:
    levelTable = Property.ResourceTable()
    OverrideLevel = Property.Level()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.GameStarted, self.onGameStart)
    
    def onGameStart(self, gEvent):
        self.gSpace = self.Owner.CreateSpace("GameSpace")
        
        if not self.OverrideLevel.Name == "DefaultLevel":
            self.gSpace.LoadLevel(self.OverrideLevel)
        else:
            self.gSpace.LoadLevel(self.levelTable.GetValueAt(0))
    
    def getCurrentLevelIndex(self):
        return self.levelTable.FindIndexOfResource(self.gSpace.CurrentLevel)
    
    def getLevelCount(self):
        return self.levelTable.Size
    
    def loadNextLevel(self):
        nextLevelID = self.getCurrentLevelIndex()
        
        totalLevels = self.getLevelCount()
        
        if nextLevelID < totalLevels-1:
            nextLevelID += 1
        
        levelResource = self.levelTable.GetResourceAt(nextLevelID)
        
        self.gSpace.LoadLevel(levelResource)
    #end loadNextLevel()
    
    def loadLevelIndex(self, index):
        totalLevels = self.getLevelCount()
        
        if index > 0 and index < totalLevels:
            levelResource = self.levelTable.GetResourceAt(index)
            self.gSpace.LoadLevel(levelResource)
    #def loadLevelIndex()
    
    def loadPreviousLevel(self):
        nextLevelID = self.getCurrentLevelIndex()
        
        totalLevels = self.getLevelCount()
        
        if nextLevelID > 0:
            nextLevelID -= 1
        
        levelResource = self.levelTable.GetResourceAt(nextLevelID)
        
        self.gSpace.LoadLevel(levelResource)
    #end loadPreviousLevel()
#endclass

Zero.RegisterComponent("LevelManager", LevelManager)