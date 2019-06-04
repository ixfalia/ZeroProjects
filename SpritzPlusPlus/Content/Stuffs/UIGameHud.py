import Zero
import Events
import Property
import VectorMath

class HUDMaker:
    DebugMode = Property.Bool(default = True)
    HUDSpace = None
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStarted)
        Zero.Connect(self.Space, "HUDCreate", self.onHUDCreate)
        
    def onLevelStarted(self, GameEvent):
        self.HUDSpace = Zero.Game.CreateNamedSpace("UI", "DefaultSpace")
        self.HUDSpace.LoadLevel("HUD")
        camera = self.HUDSpace.FindObjectByName("HUDCamera")
        GameEvent.Viewport.AddLayer(self.HUDSpace, camera)
        
        if self.DebugMode:
            print("HUDCreated Event Sent", self.HUDSpace.Name)
            
        HudCreated = Zero.ScriptEvent()
        HudCreated.HUDSpace = self.HUDSpace
        self.Space.DispatchEvent("HUDCreated", HudCreated)
        
        InfoEvent = Zero.ScriptEvent()
        InfoEvent.Space = self.Space
        self.HUDSpace.DispatchEvent("InformationEvent", InfoEvent)
        
    def getHUD(self):
        return self.HUDSpace
    
    def onHUDCreate(self, Event):
        self.HUDSpace = Event.HUDSpace
#endclass


Zero.RegisterComponent("HUDMaker", HUDMaker) 