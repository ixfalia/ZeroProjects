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
        
        PointsEvent.Points = self.Points
        self.HUDSpace.DispatchEvent("PointsEvent", PointsEvent)
        
        if self.DebugMode:
            print("Points At: ", self.Points)
    #enddef()
#endpoints

Zero.RegisterComponent("PointsCounter", PointsCounter)