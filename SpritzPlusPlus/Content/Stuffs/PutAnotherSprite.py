import Zero
import Events
import Property
import VectorMath

class PutAnotherSprite:
    DebugMode = Property.Bool(default = False)
    SpriteName = Property.String(default = "")
    Offset = Property.Vector3()
    Size = Property.Float(default = 1)
    
    mySprite = None
    
    def Initialize(self, initializer):
        if not self.SpriteName == "":
            if self.DebugMode:
                print("WaterSpin.PuteAnotherSrite.init()", self.SpriteName)
            self.mySprite = self.Space.CreateAtPosition("Sprite", self.Owner.Transform.Translation + self.Offset)
            self.mySprite.Sprite.SpriteSource = self.SpriteName
            
            if not self.Size == 0:
                self.mySprite.Transform.Scale = VectorMath.Vec3(self.Size, self.Size, self.Size)
            else:
                size = self.Owner.Transform.Scale.x
                self.mySprite.Transform.Scale = VectorMath.Vec3(size, size, size)
                
            
    
    def CreateNewSprite(self, name):
        print("making new sprite", name)
        self.mySprite.Destroy()
        self.mySprite = self.Space.CreateAtPosition("Sprite", self.Owner.Transform.Translation + self.Offset)
        self.mySprite.Sprite.SpriteSource = name
        
        #print("my sprite is", self.mySprite)
        
        if not self.Size == 0:
                self.mySprite.Transform.Scale = VectorMath.Vec3(self.Size, self.Size, self.Size)
        else:
            size = self.Owner.Transform.Scale.x
            self.mySprite.Transform.Scale = VectorMath.Vec3(size, size, size)
            

Zero.RegisterComponent("PutAnotherSprite", PutAnotherSprite)