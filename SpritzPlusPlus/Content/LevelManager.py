import Zero
import Events
import Property
import VectorMath

class LevelManager:
    levelTable = Property.ResourceTable()
    OverrideLevel = Property.Level()
    LevelSelect = Property.Level()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.GameStarted, self.onGameStart)
        print("LevelManager.Initialize()")
        self.LastPlayedLevel = self.levelTable.FindResource("Main Menu")
        
        if not self.OverrideLevel.Name == "DefaultLevel":
            self.CurrentLevel = self.OverrideLevel
        else:
            self.CurrentLevel = self.levelTable.FindResource("Main Menu")
        
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
            #self.gSpace.LoadLevel(self.levelTable.GetValueAt(0))
            self.loadLevelLevel(self.levelTable.GetValueAt(0))
    
    def getCurrentLevelIndex(self):
        return self.levelTable.FindIndexOfResource(self.gSpace.CurrentLevel)
    
    def getLastLevelIndex(self):
        return self.levelTable.FindIndexOfResource(self.LastPlayedLevel)
    
    def getLastLevel(self):
        return self.LastPlayedLevel
    
    def getLevelCount(self):
        return self.levelTable.Size
    
    def loadNextLevel(self):
        print("LevelManager.loadNextLevel()")
        nextLevelID = self.getCurrentLevelIndex()
        
        totalLevels = self.getLevelCount()
        
        if nextLevelID < totalLevels-1:
            nextLevelID += 1
        
        levelResource = self.levelTable.GetResourceAt(nextLevelID)
        
        self.loadLevelLevel(levelResource)
    #end loadNextLevel()
    
    def loadLevelIndex(self, index):
        print("LevelManager.loadLevelIndex()")
        totalLevels = self.getLevelCount()
        
        if index > 0 and index < totalLevels:
            levelResource = self.levelTable.GetResourceAt(index)
            self.loadLevelLevel(levelResource)
    #def loadLevelIndex()
    
    def loadLevelName(self, name):
        print("LevelManager.loadLevelName():")
        print("\tAttempting to load: ", name)
        
        level = Zero.ResourceSystem.GetResourceByTypeAndName("Level", name)
        
        if not level:
            raise
            return
        
        self.loadLevelLevel(levelResource)
    
    def loadLevelLevel(self, level):
        print("=======================================================================")
        print("LevelManager.loadLevelLevel():")
        print("\tLevel Set to:", level.Name)
        print("\t Last Level: ", self.LastPlayedLevel.Name)
        print("=======================================================================")
        
        self.LastPlayedLevel = self.CurrentLevel
        self.CurrentLevel = level
        self.gSpace.DestroyAll()
        self.gSpace.LoadLevel(level)
        #raise
    
    def loadPreviousLevel(self):
        print("LevelManager.loadPreviousLevel()")
        nextLevelID = self.getCurrentLevelIndex()
        
        totalLevels = self.getLevelCount()
        
        if nextLevelID > 0:
            nextLevelID -= 1
        
        levelResource = self.levelTable.GetResourceAt(nextLevelID)
        
        self.loadLevelLevel(levelResource)
    #end loadPreviousLevel()
    
    def getGameSpace(self):
        if not self.gSpace:
            self.gSpace = Zero.Game.FindSpaceByName("GameSpace")
            
            if not self.gSpace:
                return
        
        return self.gSpace
    
    def getLevel(self, index):
        return self.levelTable.GetResourceAt(index)
    
    def loadLevelSelect(self):
        if not self.LevelSelect:
            return
        
        #self.LastPlayedLevel = self.CurrentLevel
        #self.CurrentLevel = self.Level
        #levelResource = self.levelTable.GetResourceAt(nextLevelID)
        level = self.levelTable.FindResource("Level Selection")
        self.loadLevelLevel(level)
    
#endclass

Zero.RegisterComponent("LevelManager", LevelManager)