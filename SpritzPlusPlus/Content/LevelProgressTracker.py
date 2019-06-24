import Zero
import Events
import Property
import VectorMath

class LevelProgressTracker:
    def Initialize(self, initializer):
        TotalLevels = self.GameSession.LevelManager.getLevelCount()
        CurrentLevel =  self.GameSession.LevelManager.getCurrentLevelIndex()
        
        self.Owner.SpriteText.Text = "Levels: %d / %d" %(CurrentLevel-1, TotalLevels-3)

Zero.RegisterComponent("LevelProgressTracker", LevelProgressTracker)