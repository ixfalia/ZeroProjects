import Zero
import Events
import Property
import VectorMath

class GameSessionManager:
    class LevelStatistics:
        TotalFlowers = 0
        FlowersCollected = 0
        ActiveFlowers = []
    #end class LevelStatistics
    
    def Initialize(self, initializer):
        self.TotalPoints = 0
        self.LevelStats = []
        
        self.CompletedLevels = []
    #end initialize()
#end class GameSessionManager

Zero.RegisterComponent("GameSessionManager", GameSessionManager)