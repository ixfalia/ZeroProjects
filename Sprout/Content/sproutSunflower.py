import Zero
import Events
import Property
import VectorMath

import myCustomEnums
import Color

sproutTypes = myCustomEnums.sproutTypes
effectTypes = myCustomEnums.effectTypes

class sproutSunflower:
    def Initialize(self, initializer):
        self.Owner.Sprite.Color = Color.Gold
    
    def takeEffect(self, effect):
        if effect == effectTypes.sunny:
            self.bloom()
        elif effect == effectTypes.rainy:
            self.wilt()
        
    
    def bloom():
        self.Owner.Sprite.Color = Color.Gold
    
    def wilt():
        self.Owner.Sprite.Color = Color.Gold.lerp(Color.DarkSlateGray, 0.5)

Zero.RegisterComponent("sproutSunflower", sproutSunflower)