import Zero
import Events
import Property
import VectorMath

import Keys

class Cheater:
    CheatModeActive = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
    
    def onUpdate(self, uEvent):
        if Zero.Keyboard.KeyIsPressed(Keys.One) == True:
            self.ToggleCheatMode()
        
        if self.CheatModeActive:
            if Zero.Keyboard.KeyIsPressed(Keys.Two):
                self.Owner.WaterTank.ToggleUnlimitedWater()
            #endif
            
            if Zero.Keyboard.KeyIsPressed(Keys.Minus):
                #self.Owner.Teleport.GoToLastCheckpoint()
                pass
            #endif
            
            if Zero.Keyboard.KeyIsPressed(Keys.Equal):
                self.Owner.Teleport.GoToNextCheckpoint()
            
            if Zero.Keyboard.KeyIsPressed(Keys.LeftBracket):
                Zero.Game.LevelManager.loadPreviousLevel()
            
            if Zero.Keyboard.KeyIsPressed(Keys.RightBracket):
                Zero.Game.LevelManager.loadNextLevel()
            
        #endif
    #enddef
    
    def onGamepad(self, gEvent):
        pass
    
    def ToggleCheatMode(self):
        self.CheatModeActive = not self.CheatModeActive
        
        self.updateCheatMode()
    
    def updateCheatMode(self):
        #print("Cheatmode Active:", self.CheatModeActive)
        cheatEvent = Zero.ScriptEvent()
        cheatEvent.Toggle = self.CheatModeActive
        
        self.Owner.HUDEventDispatcher.DispatchHUDEvent("CheatEvent", cheatEvent)

Zero.RegisterComponent("Cheater", Cheater)