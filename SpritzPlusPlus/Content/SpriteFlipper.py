import Zero
import Events
import Property
import VectorMath

#Provides functionality to flip the sprite of and object
class SpriteFlipper:
    DebugMode = Property.Bool(default = True)
    
    isFlipped = Property.Bool(default = False)
    isFlippedY = Property.Bool(default = False)
    
    MovementBasedFlipping = Property.Bool(default = True)
    yFlipping = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
    
    def onUpdate(self, updateEvent):
        checkSpriteFlip()
    
    def checkSpriteFlip(self):
        change = self.isFlipped
        MovementVector = self.Owner.MovementController.GetMovementVector()
        
        if( self.MovementVector.x < 0 ):
            self.isFlipped = False
        elif( self.MovementVector.x > 0 ):
            self.isFlipped = True
        #endif
        
        change = change != isFlipped
    #end CheckSpriteFlip()
    
    def flipX(self):
        self.isFlipped = not self.isFlipped
        self.updateSprite()
    
    def flipY(self):
        self.isFlippedY = not self.isFlippedY
        self.updateSprite()
    
    def updateSprite(self):
        self.Owner.Sprite.FlipX = self.isFlipped
        self.Owner.Sprite.FlipY = self.isFlippedY
    
    def setFlipX(self, _isFlipped):
        self.isFlipped = _isFlipped
        self.updateSprite()
    
    def setFlipY(self, _isFlipped):
        self.isFlippedY = _isFlipped
        self.updateSprite()

Zero.RegisterComponent("SpriteFlipper", SpriteFlipper)