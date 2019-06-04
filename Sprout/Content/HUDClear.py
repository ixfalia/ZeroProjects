import Zero
import Events
import Property
import VectorMath

class HUDClear:
    def Initialize(self, initializer):
        space = Zero.Game.FindSpaceByName("HUDSpace")
        if space:
            space.Destroy()

Zero.RegisterComponent("HUDClear", HUDClear)