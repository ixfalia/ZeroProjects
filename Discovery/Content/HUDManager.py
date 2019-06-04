import Zero
import Events
import Property
import VectorMath

class HUDManager:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.GameSession, "CollectionEvent", self.onCollection)
        Zero.Connect(self.GameSession, "MarvelEvent", self.onMarvel)
        
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onCollection(self, cEvent):
        pass
    
    def onMarvel(self, mEvent):
        pass

Zero.RegisterComponent("HUDManager", HUDManager)