import Zero
import Events
import Property
import VectorMath

class HUDPointsText:
    DebugMode = Property.Bool(default = True)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "PointsEvent", self.onPoints)
        
        self.Owner.SpriteText.Text = '0'.zfill(5)
    #end init()
    
    def onPoints(self, pointEvent):
        if self.DebugMode:
            print("HUDPointsText.onPoints()")
            print(pointEvent.Points)
        #PointHUD = self.Space.FindObjectByName("Points")
        
        self.Owner.SpriteText.Text = str(int(pointEvent.Points)).zfill(5)
        
        if self.DebugMode:
            print("HUDPointsText.onPoints(): PointEvent Received, current total:", self.Owner.SpriteText.Text)
    #end onPoints
#end class

Zero.RegisterComponent("HUDPointsText", HUDPointsText)