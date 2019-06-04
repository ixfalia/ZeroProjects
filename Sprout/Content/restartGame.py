import Zero
import Events
import Property
import VectorMath

class restartGame:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
    
    def onUpdate(self, uEvent):
        if Zero.Keyboard.KeyIsPressed(Zero.Keys.Backslash):
            self.Space.ReloadLevel()

Zero.RegisterComponent("restartGame", restartGame)