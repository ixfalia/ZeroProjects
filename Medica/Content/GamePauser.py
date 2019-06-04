import Zero
import Events
import Property
import VectorMath

class GamePauser:
    def Initialize(self, initializer):
        pass
    
    def FreezeGame(self):
        self.DispatchEvent("FreezeEvent")
    
    def PauseGame(self):
        self.DispatchEvent("PauseEvent")
    
    def UnpauseGame(self):
        self.DispatchEvent("UnpauseEvent")
    
    def DispatchEvent(self, EventName):
        e = Zero.ScriptEvent()
        
        spaceDispatcher = Zero.Game.GameSpaceEventDispatcher
        spaceDispatcher.DispatchGameSpaceEvent(EventName, e)
        
        self.Space.DispatchEvent(EventName, e)

Zero.RegisterComponent("GamePauser", GamePauser)