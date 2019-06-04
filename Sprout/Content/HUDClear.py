import Zero
import Events
import Property
import VectorMath

class HUDClear:
    def Initialize(self, initializer):
        space = self.GameSession.FindSpaceByName("HUDSpace")
        if space:
            space.Destroy()

Zero.RegisterComponent("HUDClear", HUDClear)