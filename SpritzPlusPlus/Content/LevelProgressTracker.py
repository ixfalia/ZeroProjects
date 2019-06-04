import Zero
import Events
import Property
import VectorMath

class LevelProgressTracker:
    def Initialize(self, initializer):
        TotalLevels = Zero.Game.LevelManager.getLevelCount()
        CurrentLevel =  Zero.Game.LevelManager.getCurrentLevelIndex()
        
        self.Owner.SpriteText.Text = "Levels: %d / %d" %(CurrentLevel-2, TotalLevels-4)

Zero.RegisterComponent("LevelProgressTracker", LevelProgressTracker)