import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class NotificationManager:
    SpawnPoint = Property.Vector3(default = Vec3(9, 0, 1))
    
    def Initialize(self, initializer):
        pass
    
    def CreatePushMessage(self, name, message, icon, color = None, sound = None, amount = None):
        notification = self.Owner.HUDFactory.createHUDObject("PushMessage", self.SpawnPoint)
        
        notification.PushMessage.setData(name, message, icon, color, None, sound, amount)
        
        return notification

Zero.RegisterComponent("NotificationManager", NotificationManager)