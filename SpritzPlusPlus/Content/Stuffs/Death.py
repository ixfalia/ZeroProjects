import Zero
import Events
import Property
import VectorMath

class DeathMaker:
    DebugMode = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "OnPlayerAndDeath", self.onPlayerAndDeathMaker)
        
    def onPlayerAndDeathMaker(self, Event):
        if self.DebugMode:
            print("Deathmaker: Player = Dead")
        
        player = Event.GetOtherObject(self.Owner)
        PlayerDeath =  Zero.ScriptEvent()        
        #self.Space.DispatchEvent("PlayerDeath", PlayerDeath)
        player.DispatchEvent("PlayerDeath", PlayerDeath)


Zero.RegisterComponent("DeathMaker", DeathMaker)