import Zero
import Events
import Property
import VectorMath

class HUDMaker:
    DebugMode = Property.Bool(default = True)
    HUDLevel = Property.Resource("Level")
    HUDSpace = None
    
    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStarted)
        #Zero.Connect(self.Space, "HUDCreate", self.onHUDCreate)
        
        self.HUDSpace = Zero.Game.CreateNamedSpace( "HUDSpace", "Space")
        self.HUDSpace.LoadLevel(self.HUDLevel)
        
        pEvent = Zero.ScriptEvent()
        pEvent.Space = self.Space
        self.HUDSpace.DispatchEvent("GameSpaceEvent", pEvent)
        
        if self.Owner.CameraViewport:
            self.Owner.CameraViewport.Background = False
            self.Owner.CameraViewport.Layer = 1
            #self.Owner.CameraViewport.Renderer = "LevelSettings"
    #end Initialize()
    
    def Destroyed(self):
        if not self.HUDSpace:
            return
        self.HUDSpace.Destroy()
    #end def
    
    def onLevelStarted(self, GameEvent):
        self.HUDSpace = Zero.Game.CreateNamedSpace("HUDSpace", "Space")
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