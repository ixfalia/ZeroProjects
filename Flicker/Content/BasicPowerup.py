import Zero
import Events
import Property
import VectorMath
import random

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class Colors:
    def __init__(self, Color, Value):
        self.Name = Color
        self.Value = Value

class BasicPowerup:
    DebugMode = Property.Bool(default = True)
    Type = Property.String(default = "")
    Strength = Property.Float(default = 10)
    Color = Property.Vector4(default = VectorMath.Vec4(1,1,1,1))
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
        Zero.Connect(self.Owner, Events.LevelStarted, self.onLevel)
        
        Red = Colors("Red",Vec4(1,0,0,1))
        Green = Colors("Green",Vec4(0,1,0,1))
        Blue = Colors("Blue",Vec4(0,0,1,1))
        Health = Colors("Health", Vec4(0,1,1,1))
        
        self.Colors = [Red, Green, Blue, Health]
        
        color = self.selectRandomColor()
        self.Type = color.Name
        self.Color = color.Value
        
        if self.Type == "Health":
            self.Owner.Sprite.SpriteSource = "Health"
        
        self.Owner.Sprite.Color = self.Color
    #end Init()
    
    def onLevel(self, Event):
        self.Owner.Sprite.Color = self.Color
    
    def onCollision(self, Event):
        other = Event.GetOtherObject(self.Owner)
        
        if other.PlayerController:
            if self.DebugMode:
                print("BasicPowerup.onCollision() Player Detected")
                
            if self.Type == "Health":
                other.SoundEmitter.PlayCue("HealthUp")
                other.Health.healDamage(15)
            elif not self.Type == "":
                other.SoundEmitter.PlayCue("Powerup")
                other.LightTank.replenish(self.Strength, self.Type)
            
            
            
            self.Owner.Destroy()
    
    def selectRandomColor(self):
        nu = random.randint(0,len(self.Colors)-1)
        
        return self.Colors[nu]

Zero.RegisterComponent("BasicPowerup", BasicPowerup)