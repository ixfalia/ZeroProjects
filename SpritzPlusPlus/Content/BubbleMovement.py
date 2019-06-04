import Zero
import Events
import Property
import VectorMath
import Action

    #This class is used to apply a bubble drifting movement to all objects with this
    # attribute
class BubbleMovement:
    def Initialize(self, initializer):
        pass

Zero.RegisterComponent("BubbleMovement", BubbleMovement)