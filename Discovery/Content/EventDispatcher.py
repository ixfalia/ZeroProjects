import Zero
import Events
import Property
import VectorMath

class EventDispatcher:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        self.SpaceList = {}
        self.SpaceList["GameSpace"] = None
        self.SpaceList["HUDSpace"] = None
        
        self.GameSpace = None
        self.HUDSpace = None
        
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevelStart)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onLevelStart(self, lEvent):
        self.SpaceList["GameSpace"] = self.GameSession.FindSpaceByName("Space")
        pass

Zero.RegisterComponent("EventDispatcher", EventDispatcher)