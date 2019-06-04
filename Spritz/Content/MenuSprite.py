import Zero
import Events
import Property
import VectorMath

class MenuSprite:
    Source = Property.String(default = "Credits")
    def Initialize(self, initializer):
        self.Owner.Sprite.SpriteSource = self.Source
    
    def changeSprite(self, string):
        self.Owner.Sprite.SpriteSource = string

Zero.RegisterComponent("MenuSprite", MenuSprite)