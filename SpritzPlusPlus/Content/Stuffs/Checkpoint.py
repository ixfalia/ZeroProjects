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
        Zero.Connect(self.Owner, "OnPlayerAndCheckpoint", self.onPlayerAndCheckpoint)
        #Zero.Connect(
        
        pos = self.Owner.Transform.Translation
        self.Position = Vec2(pos.x, pos.y)
        
        self.Owner.SpriteText.Text = self.Owner.Name + " " + str(self.ID)
        
    def onLevelStart(self, Event):
        pos = self.Owner.Transform.Translation
        self.Position = Vec2(pos.x, pos.y)
        self.isUsed = False
        
    def onPlayerAndCheckpoint(self, Event):
        if self.isUsed:
            return
        
        other = Event.GetOtherObject(self.Owner)
        
        
        if other.Teleport:
            other.Teleport.Checkpoint = self.Position
            self.isUsed =  True
            
            self.Owner.Sprite.SpriteSource = "Checkpoint"
            
            #if self.Owner.WaterTank:
            #    self.Owner.WaterTank.Tank = 0.5
            
            if self.Owner.SoundEmitter:
                self.Owner.SoundEmitter.Play()
            
            if self.Owner.Sprite.Visible:
                flower = self.Space.CreateAtPosition("CheckpointFlower", self.Owner.Transform.Translation + Vec3(0, 2,1))
                flower.Transform.Scale = Vec3(0.75, 0.75, 0.75)
            
            if self.DebugMode:
                print("Checkpoint now set to: ", self.ID, self.Position)
                

Zero.RegisterComponent("Checkpoint", Checkpoint)