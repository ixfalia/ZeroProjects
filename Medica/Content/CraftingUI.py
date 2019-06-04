import Zero
import Events
import Property
import VectorMath

class CraftingUI:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "MouseActivateEvent", self.onActivate)
    
    def onActivate(self, e):
        print("#############################")
        print(" Crafting:")
        print("#############################")

Zero.RegisterComponent("CraftingUI", CraftingUI)