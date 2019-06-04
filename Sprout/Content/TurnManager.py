import Zero
import Events
import Property
import VectorMath

import Action

class TurnManager:
    TurnCount = Property.Uint(default = 10)
    
    def Initialize(self, initializer):
        #Zero.Connect(self.Space, "ManipulatorEvent", self.onActivate)
        Zero.Connect(self.Space, "AddTurnEvent", self.onAddTurn)
        Zero.Connect(self.Space, "RemoveTurnEvent", self.onRemoveTurn)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        
        self.updateHUD()
    
    def updateHUD(self):
        e = Zero.ScriptEvent()
        e.Turns = self.TurnCount
        self.Owner.HUDEventDispatcher.DispatchHUDEvent("TurnsEvent", e)
    
    def onLevel(self, lEvent):
        self.updateHUD()
    
    def addTurns(self, count = 1):
        self.TurnCount += count
        self.updateHUD()
        
        
        if self.TurnCount == 0:
            sE = Zero.ScriptEvent()
            sE.Sound = "LevelEnd"
            self.Space.DispatchEvent("PlaySoundEvent", sE)
            self.Space.DispatchEvent("OutOfTurns", sE)
            
            seq = Action.Sequence(self.Owner)
            Action.Delay(seq, 4)
            Action.Call(seq, self.GameSession.LevelManager.loadLevelIndex,(0))
            
            bgm = self.Space.FindObjectByName("MasterGrid").SoundEmitter
            bgm.Stop()
        elif self.TurnCount <= 5:
            sE = Zero.ScriptEvent()
            sE.Sound = "Countdown"
            self.Space.DispatchEvent("PlaySoundEvent", sE)
    
    def changeTurnCount(self, number):
        self.TurnCount = number
        self.updateHUD()
        #self.updateHUD()
    
    def countdown(self):
        self.addTurns(-1)
        e = Zero.ScriptEvent()
        self.Space.DispatchEvent("TurnIncrementEvent", e)
    
    def onActivate(self, aEvent):
        self.countdown()
        #self.updateHUD()
    
    def onAddTurn(self, aEvent):
        self.addTurns(aEvent.Turns)
    
    def onRemoveTurn(self, aEvent):
        if not aEvent.Turns:
            turns = -1
            
            e = Zero.ScriptEvent()
            self.Space.DispatchEvent("TurnIncrementEvent", e)
        else:
            turns = aEvent.Turns
            
        self.addTurns(turns)

Zero.RegisterComponent("TurnManager", TurnManager)