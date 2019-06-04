import Zero
import Events
import Property
import VectorMath

Controllers = Property.DeclareEnum("Controllers", ["Controller1","Controller2", "Controller3", "Controller4"])

class GamepadController:
    def DefineProperties(self):
        self.Active = Property.Bool(default = True)
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def checkGamepad(self, controller = Controllers.Controller1):
        pass

Zero.RegisterComponent("GamepadController", GamepadController)