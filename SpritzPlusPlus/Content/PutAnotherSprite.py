import Zero
import Events
import Property
import VectorMath

class PutAnotherSprite:
    DebugMode = Property.Bool(default = False)
    SpriteSource = Property.SpriteSource()
    Offset = Property.Vector3()
    Size = Property.Float(default = 1)
    
    mySprite = None
    
    def Initialize(self, initializer):
        if not self.SpriteSource == None:
            if self.DebugMode:
                print("WaterSpin.PuteAnotherSrite.init()", self.SpriteSource.Name)
            
            if self.Owner.Transform.Translation.z == 0:
                self.Owner.Transform.Translation -= VectorMath.Vec3(0,0,1)
            #endif
            
            self.mySprite = self.Space.CreateAtPosition("Sprite", self.Owner.Transform.Translation + self.Offset)
            self.finalPosition = self.Owner.Transform.Translation + self.Offset
            self.mySprite.Sprite.SpriteSource = self.SpriteSource
            self.mySprite.Sprite.Visible = True
            
            if self.DebugMode:
                print("\t* main Object at position: ", self.Owner.Transform.Translation)
                print("\t* new Sprite created: ", self.mySprite.Sprite.SpriteSource.Name, "at position:", self.mySprite.Transform.Translation)
            
            if not self.Size == 0:
                self.mySprite.Transform.Scale = VectorMath.Vec3(self.Size, self.Size, self.Size)
            else:
                size = self.Owner.Transform.Scale.x
                self.mySprite.Transform.Scale = VectorMath.Vec3(size, size, size)
            
            Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
    #end initialize()
    
    def onUpdate(self, updateEvent):
        if not self.Owner.Transform.Translation.z == self.finalPosition.z and self.Owner.FlowerSpin:
            self.Owner.Transform.Translation = self.finalPosition
        #endif
        myPosition = VectorMath.Vec2(self.mySprite.Transform.Translation)
        basePosition = VectorMath.Vec2(self.Owner.Transform.Translation)
        
        if not myPosition == basePosition:
            self.mySprite.Transform.Translation = VectorMath.Vec3(basePosition.x, basePosition.y, 12)
        #event
    #onUpdate()
    
    def CreateNewSprite(self, name):
        if self.DebugMode:
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