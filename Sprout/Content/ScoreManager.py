import Zero
import Events
import Property
import VectorMath

class ScoreManager:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "ComboEvent", self.onCombo)
        self.currentScore = 0
        self.highScore = 0
    
    def onCombo(self, cEvent):
        comboManager = self.Owner.ComboTracker
        length = cEvent.ChainLength
        
        if length >= 4:
            points = length * (length-1) * 10 + (1*comboManager.comboFever)
        else:
            points = length * 20
        
        self.currentScore += points
        
        e = Zero.ScriptEvent()
        e.currentScore = self.currentScore
        self.Owner.HUDEventDispatcher.DispatchHUDEvent("ScoreEvent", e)

Zero.RegisterComponent("ScoreManager", ScoreManager)