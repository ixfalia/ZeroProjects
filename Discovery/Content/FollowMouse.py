import Zero
import Events
import Property
import VectorMath

class FollowMouse:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Active = Property.Bool(default = True)
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        position = self.getMouseWorldPosition(self.Owner.Transform.Translation.z)
        
        self.Owner.Transform.Translation = position
        pass
    
    def getMouseWorldPosition(self, zPos = 3):
        mouse = Zero.Mouse
        viewport = self.Space.FindObjectByName("LevelSettings").CameraViewport
        worldposition = viewport.ScreenToWorldZPlane(mouse.ScreenPosition, zPos)
        
        return worldposition

Zero.RegisterComponent("FollowMouse", FollowMouse)