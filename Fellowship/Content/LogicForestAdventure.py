import Zero
import Events
import Property
import VectorMath

class LogicForestAdventure:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, "TimeIncrementEvent", self.onTimeIncrement)
        Zero.Connect(self.Space, "NextEvent", self.onNext)
        self.AdventureLogic = self.Owner.AdventureLogic
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def FirstChallenge(self):
        self.CheckDifficulty = 11
        result = self.AdventureLogic.StatCheck("Speed")
        byHowMuch = result - self.CheckDifficulty
        
        isSuccess = result > self.CheckDifficulty
        
        staminaDepletion = 0
        
        if isSuccess:
            higher = max(self.GameSession.Statistics.Resistance, self.GameSession.Statistics.Defense)
            staminaDepletion = 0.25 * (1 - higher)
    
    def onTimeIncrement(self, TimeEvent):
        pass
    
    def onNext(self, NextEvent):
        pass
    

Zero.RegisterComponent("LogicForestAdventure", LogicForestAdventure)