import Zero
import Events
import Property
import VectorMath

class ColorBase:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.useSpriteColor = Property.Bool()
        
        self.Color = Property.Color()
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        if self.useSpriteColor:
            self.Color = self.Owner.Sprite.Color
        
        self.StartingColor = self.Color
        self.OldColor = self.Color

    def OnLogicUpdate(self, UpdateEvent):
        if not self.OldColor == self.Color:
            raise
        
        self.OldColor = self.Color
    
    def ChangeColor(self, Color):
        self.Color = Color
        
        self.UpdateColor()
    
    def ResetColor(self):
        self.ChangeColor(self.StartingColor)
    
    def UpdateColor(self):
        self.Owner.Sprite.Color = self.Color

Zero.RegisterComponent("ColorBase", ColorBase)