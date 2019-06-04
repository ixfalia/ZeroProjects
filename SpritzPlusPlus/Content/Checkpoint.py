import Zero
import Events
import Property
import VectorMath

import Color

Vec3 = VectorMath.Vec3
Vec2 = VectorMath.Vec2

checkpointCount = 0

class Checkpoint:
    DebugMode = Property.Bool(default = False)
    ID = Property.Uint(default = 0)
    Position = Property.Vector2()
    textVisible = Property.Bool(default = False)
    
    isUsed = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        Zero.Connect(self.Owner, "OnPlayerAndCheckpoint", self.onPlayerAndCheckpoint)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        #Zero.Connect(
        
        pos = self.Owner.Transform.Translation
        self.Position = Vec2(pos.x, pos.y)
        #self.ID = self.ID
        global checkpointCount
        self.ID = checkpointCount
        checkpointCount += 1
        
        if not self.Owner.SpriteText == None:
            self.Owner.SpriteText.Text = self.Owner.Name + " " + str(self.ID)
            self.Owner.SpriteText.Visible = self.textVisible
    
    def onLevelStart(self, Event):
        global checkpointCount
        checkpointCount = 0
        
        pos = self.Owner.Transform.Translation
        self.Position = Vec2(pos.x, pos.y)
        self.isUsed = False
    
    def onCollision(self, Event):
        other = Event.OtherObject
        
        if other.Collider.CollisionGroup.Name == "Player":
            self.onPlayerAndCheckpoint(Event)
    
    def onPlayerAndCheckpoint(self, Event):
        if self.isUsed:
            return
        
        other = Event.OtherObject
        
        
        if other.Teleport:
            other.Teleport.Checkpoint = self.Position
            self.isUsed =  True
            offset = Vec3(0,3,0.5)
            
            self.Owner.Sprite.SpriteSource = "Checkpoint"
            #self.Owner.Sprite.Color = Color.Green
            self.Space.CreateAtPosition("WaterEffect", self.Owner.Transform.Translation + offset)
            
            #if self.Owner.WaterTank:
            #    self.Owner.WaterTank.Tank = 0.5
            
            if self.Owner.SoundEmitter:
                self.Owner.SoundEmitter.Play()
            
            if self.Owner.Sprite.Visible:
                flower = self.Space.CreateAtPosition("CheckpointFlower", self.Owner.Transform.Translation + offset)
                flower.Transform.Scale = Vec3(0.75, 0.75, 0.75)
            
            if self.DebugMode:
                print("Checkpoint now set to: ", self.ID, self.Position)
                

Zero.RegisterComponent("Checkpoint", Checkpoint)