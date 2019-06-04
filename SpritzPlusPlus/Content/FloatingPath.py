import Zero
import Events
import Property
import VectorMath

class FloatingPath:
    ID = Property.Int(default = 0)
    
    def Initialize(self, initializer):
        pass

Zero.RegisterComponent("FloatingPath", FloatingPath)