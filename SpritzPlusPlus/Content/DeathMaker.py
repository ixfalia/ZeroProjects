import Zero
import Events
import Property
import VectorMath

class DeathMaker:
    DebugMode = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "OnPlayerAndDeath", self.onPlayerAndDeathMaker)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        
    def onPlayerAndDeathMaker(self, Event):
        if self.DebugMode:
            print("Deathmaker: Player = Dead")
        
        player = Event.OtherObject
        PlayerDeath =  Zero.ScriptEvent()
        #self.Space.DispatchEvent("PlayerDeath", PlayerDeath)
        player.DispatchEvent("PlayerDeath", PlayerDeath)
        
    def onCollision(self, collisionEvent):
        other = collisionEvent.OtherObject
        
        if other.Player:
            PlayerDeath =  Zero.ScriptEvent()
            other.DispatchEvent("PlayerDeath", PlayerDeath)
            #raise
        


Zero.RegisterComponent("DeathMaker", DeathMaker)