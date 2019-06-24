import Zero
import Events
import Property
import VectorMath

class EndLevel:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
    
    def onGamepad(self, gEvent):
        if(gEvent.Button == Zero.Buttons.DpadUp or gEvent.Button == Zero.Buttons.DpadDown
        or gEvent.Button == Zero.Buttons.DpadLeft or gEvent.Button == Zero.Buttons.DpadRight):
            return
        
        self.GameSession.LevelManager.loadLevelIndex(1)

Zero.RegisterComponent("EndLevel", EndLevel)