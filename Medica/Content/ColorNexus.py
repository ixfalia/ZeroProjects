import Zero
import Events
import Property
import VectorMath

class ColorNexus:
    BaseColor = Property.Color()
    
    def Initialize(self, initializer):
        pass

Zero.RegisterComponent("ColorNexus", ColorNexus)