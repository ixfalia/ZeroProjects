import Zero
import Events
import Property
import VectorMath
import Action

class CameraController:
    DebugMode = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "GameViewportUpdate", self.OnGameViewportUpdate)
    #end Initialize()
    
    def OnGameViewportUpdate(self, GameViewportEvent):
        GameViewportEvent.Viewport.Camera = self.Owner.Camera
        #Get the CameraGroupFocuser component on ourself
        self.Focuser = self.Owner.CameraGroupFocuser

        #Attempt to find the object named "MainCharacter"
        player = self.Space.FindObjectByName("MainCharacter")
        #Set the CameraGroupFocuser to follow the Player
        self.Focuser.AddObject(player)
    #end OnGameViewportUpdate()

#end class CameraController

Zero.RegisterComponent("CameraController", CameraController)