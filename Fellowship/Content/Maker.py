import Zero
import Events
import Property
import VectorMath

class Maker:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.CreateAtStart = Property.Bool(default = True)
        self.DetectedEvent = Property.String()
        
        self.Object = Property.Archetype()
        self.Position = Property.Vector3()
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        
        if not self.onEvent == "":
            Zero.Connect(self.Owner, self.DetectedEvent, self.onEvent)
        self.Created = None
        pass
    
    def onLevel(self, LevelEvent):
        if self.CreateAtStart:
            self.Make()
    
    def Make(self):
        self.Created = self.Space.CreateAtPosition(self.Object, self.Position)

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onEvent(self, Event):
        self.Make()

Zero.RegisterComponent("Maker", Maker)