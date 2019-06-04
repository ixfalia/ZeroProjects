import Zero
import Events
import Property
import VectorMath
import PlayerController

#Useful Variables
Keys = Zero.Keys
Keyboard = Zero.Keyboard
Vec3 = VectorMath.Vec3

class KeyboardController:
    DebugMode = Property.Bool(default = False)
    MovementFrame = Vec3()
    
    def Initialize(self, initializer):
        pass

Zero.RegisterComponent("KeyboardController", KeyboardController)