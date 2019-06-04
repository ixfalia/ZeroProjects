import Zero
import Events
import Property
import VectorMath

class GameStateTracker: 
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, "PetUpdateEvent", self.onPetUpdate)
        
        self.Statistics
        pass

    def UpdateGameData(self):
        #self.Owner.DispatchEvent("RequestPetData", Zero.ScriptEvent())
        pass
    
    def onPetUpdate(self, PetEvent):
        stats = PetEvent.Sender.Statistics

Zero.RegisterComponent("GameStateTracker", GameStateTracker)