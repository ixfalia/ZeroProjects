import Zero
import Events
import Property
import VectorMath

class LocationTrigger:
    Location = Property.String()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
    
    def onCollision(self, e):
        other = e.OtherObject
        
        if other.MovementController:
            self.LocationEntered()
    
    def LocationEntered(self):
        obj = Zero.Game.HUDFactory.createHUDObject("LocationMessage", VectorMath.Vec3(0, 9, 4))
        obj.SpriteText.Text = self.Location
        obj.Fader.FadeIn()

Zero.RegisterComponent("LocationTrigger", LocationTrigger)