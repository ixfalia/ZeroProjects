import Zero
import Events
import Property
import VectorMath

class ScoreTracker:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "ScoreEvent", self.onScore)
        self.CurrentScore = 0
        
        self.updateText()
    
    def onScore(self, tEvent):
        self.CurrentScore = tEvent.currentScore
        
        self.updateText()
    
    def updateText(self):
        self.Owner.SpriteText.Text = "{0}".format(self.CurrentScore)

Zero.RegisterComponent("ScoreTracker", ScoreTracker)