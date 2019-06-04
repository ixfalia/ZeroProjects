import Zero
import Events
import Property
import VectorMath

class DetectController:
    def Initialize(self, initializer):
        self.gamepad = Zero.Gamepads
        pass

Zero.RegisterComponent("DetectController", DetectController)