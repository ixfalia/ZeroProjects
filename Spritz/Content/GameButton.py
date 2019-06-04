import Zero
import Events
import Property
import VectorMath

class GameButton:
    isReset = Property.Bool(default=False)
    isQuit = Property.Bool(default=False)
    
    HUDManager = None
    def Initialize(self, initializer):
        self.HUDManager = self.Space.FindObjectByName("HUDController")
        
    def do(self):
        if self.HUDManager == None:
            self.HUDManager = self.Space.FindObjectByName("HUDController")
        
        if self.isReset:
            self.HUDManager.Do("Reset")
        elif self.isQuit:
            self.HUDManager.Do("Quit")

Zero.RegisterComponent("GameButton", GameButton)