import Zero
import Events
import Property
import VectorMath

class Teleport:
    DebugMode = Property.Bool(default = False)
    Checkpoint = Property.Vector2()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        #Zero.Connect(self.Owner, "PlayerDeath", self.onPlayerDeath)
        
    def onLevelStart(self, Event):
        startpoint = self.Space.FindObjectByName("Start")
        
        if startpoint.Checkpoint:
            self.Checkpoint = startpoint.Checkpoint.Position
            self.TeleportMe(self.Checkpoint)
            
    def GoToCheckpoint(self):
        self.TeleportMe(self.Checkpoint)
    
    def TeleportMe(self, place):
        if( self.Owner.Transform ):
            self.Owner.Transform.Translation = place
            
    def setCheckpoint(self, place):
        if self.DebugMode:
            print("Checkpoint set to:", place)
            
        self.Checkpoint = place
        
    def onPlayerDeath(self, Event):
        self.Owner.Transform.Translation = self.Checkpoint

Zero.RegisterComponent("Teleport", Teleport)