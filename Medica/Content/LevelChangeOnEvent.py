import Zero
import Events
import Property
import VectorMath

class LevelChangeOnEvent:
    EventString = Property.String()
    Level = Property.Level()
    
    def Initialize(self, initializer):
        Zero.Connect(Zero.Game, self.EventString, self.onEvent)
    
    def onEvent(self, e):
        self.Space.DestroyAll()
        self.Space.LoadLevel(self.Level)

Zero.RegisterComponent("LevelChangeOnEvent", LevelChangeOnEvent)