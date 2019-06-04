import Zero
import Events
import Property
import VectorMath

class TestHUD:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, "Whoo", self.onWhoo)
        
        e = Zero.ScriptEvent()
        e.EventType = "Whoo"
        e.Event = Zero.ScriptEvent()
        self.Space.DispatchEvent("HUDRouteEvent", e)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onWhoo(self, wEvent):
        print(self.Space.Name)
        print(self.GameSession.FindSpaceByName("Main"))
        raise

Zero.RegisterComponent("TestHUD", TestHUD)