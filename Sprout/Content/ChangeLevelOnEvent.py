import Zero
import Events
import Property
import VectorMath

class ChangeLevelOnEvent:
    Event = Property.String()
    Level = Property.Level()
    
    def Initialize(self, initializer):
        if not self.Event == "":
            Zero.Connect(self.Space, self.Event, self.onEvent)
    
    def onEvent(self, eEvent):
        if not self.Level.Name == "DefaultLevel":
            self.Space.LoadLevel(self.Level)

Zero.RegisterComponent("ChangeLevelOnEvent", ChangeLevelOnEvent)