import Zero
import Events
import Property
import VectorMath

class MapUI:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "MouseActivateEvent", self.onActivate)
    
    def onActivate(self, e):
        print("[][][][][][][][][][][][][]")
        print("Map:")
        print("[][][][][][][][][][][][][]")

Zero.RegisterComponent("MapUI", MapUI)