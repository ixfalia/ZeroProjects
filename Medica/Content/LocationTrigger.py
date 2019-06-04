import Zero
import Events
import Property
import VectorMath

class LocationTrigger:
    Location = Property.String()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.onCollisionEnd)
        
        self.Sign = None
    
    def onCollision(self, e):
        other = e.OtherObject
        
        if other.MovementController:
            self.LocationEntered()
        
    def onCollisionEnd(self, e):
        if self.Sign:
            self.Sign.Fader.FadeDestroy()
    
    def LocationEntered(self):
        self.Sign = Zero.Game.HUDFactory.createHUDObject("LocationMessage", VectorMath.Vec3(0, 9, 4))
        self.Sign.SpriteText.Text = self.Location
        self.Sign.Fader.FadeIn()
        
        entries = Zero.Game.Journal.LocationFlags
        
        if not self.Location in entries:
            Zero.Game.Journal.addEntry(self.Location, "Location")

Zero.RegisterComponent("LocationTrigger", LocationTrigger)