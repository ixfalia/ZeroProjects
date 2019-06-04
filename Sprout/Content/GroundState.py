import Zero
import Events
import Property
import VectorMath

import Color

class GroundState:
    Poisoned = Property.Bool(default = False)
    def Initialize(self, initializer):
        self.Poisonstrength = 0
    
    def poison(self):
        self.Owner.Sprite.Color = ground.Sprite.Color = Color.Purple.lerp(Color.White, 0.5)
        self.Poisonstrength += 1
    
    def poisona(self):
        self.Owner.Sprite.Color = Color.White
        self.Poisonstrength -= 1

Zero.RegisterComponent("GroundState", GroundState)