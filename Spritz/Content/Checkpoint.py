import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3
Vec2 = VectorMath.Vec2

class Checkpoint:
    DebugMode = Property.Bool(default = False)
    ID = Property.Uint(default = 0)
    Position = Property.Vector2()
    
    isUsed = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        Zero.Connect(self.Owner, "onPlayerAndCheckpoint", self.onPlayerAndCheckpoint)
        #Zero.Connect(self.Owner, "onCheckpointAndWater", self.onPlayerAndCheckpoint)
        Zero.Connect(self.Space, "TeleportMe", self.onTeleportMe)
        
        if self.DebugMode:
            print("Checkpoint.Initialize()")
        
        pos = self.Owner.Transform.Translation
        self.Position = Vec2(pos.x, pos.y)
        self.label = self.Owner.Name + " " + str(self.ID)
        
        if self.Owner.SpriteText:
            self.Owner.SpriteText.Text = self.Owner.Name + " " + str(self.ID)
        
        if self.DebugMode:
            print("\t", self.label, " initialized at: ", self.Position)
        
        checkEvent = Zero.ScriptEvent()
        checkEvent.ID = self.ID
        checkEvent.Position = self.Position
        checkEvent.Name = self.label
        self.Space.DispatchEvent("CheckpointEvent", checkEvent)
        
        self.Space.CreateAtPosition("CheckpointEffect", self.Owner.Transform.Translation + Vec3(0,2,0))
    #end init()
    
    def onTeleportMe(self, tEvent):
        if tEvent.ID == self.ID:
            tEvent.Teleport.TeleportMe(self.Position)
    
    def onLevelStart(self, Event):
        pos = self.Owner.Transform.Translation
        self.Position = Vec2(pos.x, pos.y)
        self.isUsed = False
        
        if self.DebugMode:
            print("\t", self.label, " initialized at: ", self.Position)
    #end onLevelStart()
    
    def onPlayerAndCheckpoint(self, Event):
        if self.isUsed:
            return
        
        other = Event.OtherObject
        
        if other.Teleport:
            other.Teleport.Checkpoint = self.Position
            other.Teleport.CurrentCheckpoint = self.ID
            
            if self.DebugMode:
                print("Checkpoint.onPlayerAndCheckpoint(): Player Checkpoint Changed")
            
            self.isUsed =  True
            
            self.Owner.Sprite.SpriteSource = "Checkpoint"
            self.Owner.Transform.Scale = VectorMath.Vec3(0.55,0.55,0.55)
            self.Owner.Transform.Translation += VectorMath.Vec3(0, -0.38, 0)
            
            #if self.Owner.WaterTank:
            #    self.Owner.WaterTank.Tank = 0.5
            
            if self.Owner.SoundEmitter:
                self.Owner.SoundEmitter.Play()
            
            if self.Owner.Sprite.Visible:
                flower = self.Space.CreateAtPosition("CheckpointFlower", self.Owner.Transform.Translation + Vec3(0,3.5,1))
                flower.Transform.Scale = Vec3(0.7, 0.7, 0.7)
                #flower.ChangeColor.ChangeColor()
            
            if self.DebugMode:
                print("Checkpoint now set to: ", self.ID, self.Position)
            
            CheckpointEvent = Zero.ScriptEvent()
            self.Owner.DispatchEvent("CheckpointActive", CheckpointEvent)

Zero.RegisterComponent("Checkpoint", Checkpoint)