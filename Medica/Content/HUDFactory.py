import Zero
import Events
import Property
import VectorMath

class HUDFactory:
    def Initialize(self, initializer):
        if self.Owner.LevelManager:
            Zero.Connect(self.Owner, "CreateHUDObject", self.onCreateHUDObj)
        else:
            Zero.Connect(self.Space, "CreateHUDObject", self.onCreateHUDObj)
    
    def createHUDObject(self, object, offset):
        HUD = Zero.Game.LevelManager.getHUDSpace()
        
        created = HUD.CreateAtPosition(object, offset)
        return created
    
    def onCreateHUDObj(self, hEvent):
        spaceDispatcher = Zero.Game.GameSpaceEventDispatcher
        
        if hEvent.Pause:
            self.pauseGame()
        elif hEvent.Freeze:
            self.freezeGame()
        
        object = hEvent.Object
        offset = hEvent.Offset
        
        if not offset:
            offset =  VectorMath.Vec3()
        
        self.createHUDObject(object, offset)
    
    def pauseGame(self):
        e = Zero.ScriptEvent()
        #spaceDispatcher.DispatchGameSpaceEvent("PauseEvent", e)
        self.Space.DispatchEvent("PauseEvent", e)
    
    def freezeGame(self):
        e = Zero.ScriptEvent()
        #spaceDispatcher.DispatchGameSpaceEvent("FreezeEvent", e)
        self.Space.DispatchEvent("FreezeEvent", e)

Zero.RegisterComponent("HUDFactory", HUDFactory)