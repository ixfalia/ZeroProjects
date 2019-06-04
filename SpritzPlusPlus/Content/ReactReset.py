import Zero
import Events
import Property
import VectorMath

class ReactReset:
    Level = Property.String(default = "")
    def Initialize(self, initializer):
        Zero.Connect( self.Space, "myGamepadEvent", self.gamepad)
    
    def gamepad(self, Event):
        if Event.Button == Zero.Buttons.A or Event.Button == Zero.Buttons.Start:
            self.Space.DestroyAllFromLevel()
            self.Space.LoadLevel(self.Level)

Zero.RegisterComponent("ReactReset", ReactReset)