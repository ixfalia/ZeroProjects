import Zero
import Events
import Property
import VectorMath

class PlayerTracker:
    def DefineProperties(self):
        PlayerName = Property.String(default = "Player")

    def Initialize(self, initializer):
        self.Player = None
        self.Viewport = None
        self.Camera = None
        
        Zero.Connect(self.Owner, Events.LevelStarted, self.onLevel)
        Zero.Connect(self.Owner, "PlayerCreationEvent", self.onPlayer)
        Zero.Connect(self.Owner, "CameraCreationEvent", self.onCamera)
        pass
    
    def onLevel(self, lEvent):
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onPlayer(self, pEvent):
        self.Player = pEvent.Player
    
    def onCamera(self, cEvent):
        self.Camera = cEvent.Camera
    
    def getPlayer(self):
        if not self.Player:
            e = Zero.ScriptEvent()
            e.Target = self.Owner
            self.Owner.DispatchEvent(e, "PlayerPollEvent")
            
            return None
        else:
            return self.Player

Zero.RegisterComponent("PlayerTracker", PlayerTracker) 