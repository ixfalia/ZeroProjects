import Zero
import Events
import Property
import VectorMath

class LevelManager:
    levelTable = Property.ResourceTable()
    OverrideLevel = Property.Level()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.GameStarted, self.onGameStart)
        self.gSpace = None
    
    def onGameStart(self, gEvent):
        
        self.gSpace = self.Owner.CreateSpace("GameSpace")
        #self.gSpace = Zero.Game.FindSpaceByName("GameSpace")
        self.gSpace.DestroyAll()
        space = Zero.Game.FindSpaceByName("Space")
        
        if not self.OverrideLevel.Name == "DefaultLevel":
            self.gSpace.LoadLevel(self.OverrideLevel)
        else:
            #print(self.levelTable.GetValueAt(0))
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
            self.gSpace.DestroyAll()
            self.gSpace.LoadLevel(levelResource)
    #def loadLevelIndex()
    
    def loadLevelName(self, name):
        level = Zero.ResourceSystem.GetResourceByTypeAndName("Level", name)
        
        if not level:
            raise
            return
        
        #levelResource = self.levelTable.FindIndexOfResource(level)
        self.gSpace.DestroyAll()
        self.gSpace.LoadLevel(level)
    
    def loadPreviousLevel(self):
        nextLevelID = self.getCurrentLevelIndex()
        
        totalLevels = self.getLevelCount()
        
        if nextLevelID > 0:
            nextLevelID -= 1
        
        levelResource = self.levelTable.GetResourceAt(nextLevelID)
        
        self.gSpace.DestroyAll()
        self.gSpace.LoadLevel(levelResource)
    #end loadPreviousLevel()
    def getGameSpace(self):
        if not self.gSpace:
            self.gSpace = Zero.Game.FindSpaceByName("GameSpace")
            
            if not self.gSpace:
                return
        
        return self.gSpace
#endclass

Zero.RegisterComponent("LevelManager", LevelManager)