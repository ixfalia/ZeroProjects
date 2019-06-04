import Zero
import Events
import Property
import VectorMath

class TurnsTracker:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "TurnsEvent", self.onTurns)
        
        self.TurnsRemaining = 0
        
        self.updateText()
    
    def onTurns(self, tEvent):
        self.TurnsRemaining = tEvent.Turns
        
        if self.TurnsRemaining == 0:
            self.Space.Create("OutOfTurns")
        self.updateText()
    
    def updateText(self):
        self.Owner.SpriteText.Text = "{0}".format(self.TurnsRemaining)

Zero.RegisterComponent("TurnsTracker", TurnsTracker)