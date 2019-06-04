import Zero
import Events
import Property
import VectorMath


class Teleport:
    DebugMode = Property.Bool(default = False)
    Checkpoint = Property.Vector2()
    CurrentCheckpoint = Property.Uint(default = 0)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        Zero.Connect(self.Space, "CheckpointEvent", self.onCheckpointEvent)
        #Zero.Connect(self.Owner, "onPlayerAndDeathMaker", self.onPlayerDeath)
        #Zero.Connect(self.Owner, "PlayerDeath", self.onPlayerDeath)
        
        self.CheckpointList = []
        self.cIterator = iter(self.CheckpointList)
        
    def onLevelStart(self, Event):
        startpoint = self.Space.FindObjectByName("TestStart")
        if not startpoint:
            startpoint = self.Space.FindObjectByName("Start")
            
            if not startpoint:
                raise
        
        if startpoint.Checkpoint:
            self.Checkpoint = startpoint.Checkpoint.Position
            self.TeleportMe(self.Checkpoint)
            
    def GoToCheckpoint(self, ID = None):
        if ID == None:
            self.TeleportMe(self.Checkpoint)
        else:
            place = self.CheckpointList[ID]#.Position
            self.TeleportMe(place)
    
    def GoToNextCheckpoint(self):
        i = self.cIterator.__next__()
        
        self.TeleportMe(i)
        teleEvent = Zero.ScriptEvent()
        
        teleEvent.ID = self.CurrentCheckpoint + 1
        teleEvent.Teleport = self
        
        self.Space.DispatchEvent("TeleportMe", teleEvent)
    
    def GoToLastCheckpoint(self):
        teleEvent = Zero.ScriptEvent()
        
        teleEvent.ID = self.CurrentCheckpoint - 1
        teleEvent.Teleport = self
        
        self.Space.DispatchEvent("TeleportMe", teleEvent)
    
    def TeleportToCheckpointID(self, ID = None):
        if ID == None:
            ID = self.CurrentCheckpoint
        
        teleEvent = Zero.ScriptEvent()
        
        teleEvent.ID = ID
        self.Space.DispatchEvent("TeleportMe", teleEvent)
    #enddef
    
    def CheatPort(self, place):
        if( self.Owner.Transform ):
            self.Owner.Transform.Translation = place
            self.Owner.RigidBody.Velocity = VectorMath.Vec3(0,0,0)
    #enddef
    
    def TeleportMe(self, place):
        if( self.Owner.Transform ):
            self.Owner.Transform.Translation = place
            self.Owner.RigidBody.Velocity = VectorMath.Vec3(0,0,0)
            
            offset = VectorMath.Vec3(0,3,0.5)
            self.Space.CreateAtPosition("WaterEffect", self.Owner.Transform.Translation + offset)
    def setCheckpoint(self, place):
        if self.DebugMode:
            print("Checkpoint set to:", place)
            
        self.Checkpoint = place
        
    def onPlayerDeath(self, Event):
        #self.Owner.Transform.Translation = self.Checkpoint
        self.GoToCheckpoint()
    
    def onCheckpointEvent(self, cEvent):
        #print("Checkpoint:", cEvent.ID, "Name:", cEvent.Name, "Position:", cEvent.Position)
        #self.CheckpointList[cEvent.ID] = cEvent.Position
        self.CheckpointList.insert(cEvent.ID, cEvent.Position)
        self.cIterator = iter(self.CheckpointList)
        print(self.CheckpointList)

Zero.RegisterComponent("Teleport", Teleport)