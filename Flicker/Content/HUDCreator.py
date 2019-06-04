import Zero
import Events
import Property
import VectorMath

class UIMaker:
    DebugMode = Property.Bool(default = True)
    HUDSpace = None
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStarted)
        Zero.Connect(self.Space, "HUDCreated", self.onHUDCreated)
        
    def onLevelStarted(self, GameEvent):
        self.HUDSpace = Zero.Game.CreateNamedSpace("UI", "DefaultSpace")
        self.HUDSpace.LoadLevel("UI")
        camera = self.HUDSpace.FindObjectByName("UICamera")
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
    
    def onHUDCreated(self, Event):
        self.HUDSpace = Event.HUDSpace
    
    def DispatchToHUDSpace(self, Name, Event):
        if self.HUDSpace:
            self.HUDSpace.DispatchEvent(Name, Event)
        else:
            print("UIMaker.DispatchToHUDSpace() HUDSpace is currently NONE Type")
#endclass


Zero.RegisterComponent("UIMaker", UIMaker) 