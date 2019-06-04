import Zero
import Events
import Property
import VectorMath

class Traction:
    # The traction (slipperyness) 
    Traction = Property.Float(1.0);
    
    # No need to do anything
    def Initialize(self, initializer):
        pass

Zero.RegisterComponent("Traction", Traction)