import Zero
import Events
import Property
import VectorMath

import myCustomEnums
import Color

sproutTypes = myCustomEnums.sproutTypes
effectTypes = myCustomEnums.effectTypes

class sproutWaterberry:
    def Initialize(self, initializer):
        self.Owner.Sprite.Color = Color.CadetBlue
    
    def takeEffect(self, effect):
        if effect == effectTypes.sunny:
            self.wilt()
        elif effect == effectTypes.rainy:
            self.bloom()
        
    
    def bloom():
        self.Owner.Sprite.Color = Color.CadetBlue
    
    def wilt():
        self.Owner.Sprite.Color = Color.CadetBlue.lerp(Color.SaddleBrown, 0.5)

Zero.RegisterComponent("sproutWaterberry", sproutWaterberry)