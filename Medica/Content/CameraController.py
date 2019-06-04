import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class CameraController:
    Target = Property.Cog()
    Offset = Property.Vector3(default = Vec3())
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
    
    def onUpdate(self, e):
        targetPosition = self.Target.Transform.Translation
        position =  Vec3(targetPosition.x, targetPosition.y, 40)
        self.Owner.Transform.Translation = position
        
        #print("Camera Position:", self.Owner.Transform.Translation)

Zero.RegisterComponent("CameraController", CameraController)