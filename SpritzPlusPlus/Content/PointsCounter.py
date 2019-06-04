import Zero
import Events
import Property
import VectorMath

class PointsCounter:
    DebugMode = Property.Bool( default = False )
    Points = Property.Uint( default = 0 )
    HUDSpace = None
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "HUDCreated", self.onHUDCreate)
    
    def onHUDCreate(self, Event):
        self.HUDSpace = Event.HUDSpace
    #end
    
    def AddPoints(self, points):
        self.Points += points
        
        PointsEvent = Zero.ScriptEvent()
        
        PointsEvent.Points = int(self.Points)
        
        #player = self.Space.FindObjectByName("MainCharacter")
        
        #if player:
        #    player.HUDEventDispatcher.SendtoHUD("PointsEvent", PointsEvent)
        
        self.Owner.HUDEventDispatcher.DispatchHUDEvent("PointsEvent", PointsEvent)
        Zero.Game.DispatchEvent("PointsEvent", PointsEvent)
        
        if self.DebugMode:
            print("Points At: ", self.Points)
    #enddef()
#endpoints

Zero.RegisterComponent("PointsCounter", PointsCounter)