import Zero
import Events
import Property
import VectorMath

Modes = Property.DeclareEnum("Moods", ["Play", "Train", "Fight", "Normal"])

class ModeController:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.CurrentMode = Property.Enum()
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass

Zero.RegisterComponent("ModeController", ModeController)