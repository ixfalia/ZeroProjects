import Zero
import Events
import Property
import VectorMath

class HUDDispatcher:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Space, "HUDRouteEvent", self.onHUDRoute);
        Zero.Connect(self.Space, "HUDInformationEvent", self.onHUDInformation)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onHUDRoute(self, HUDEvent):
        eventData = HUDEvent.Event
        eventType = HUDEvent.EventType
        
        self.Owner.HUDCreator.HUDSpace.DispatchEvent(eventType, eventData)
        #self.Owner.HUDCreator.HUDSpace.DispatchEvent(eventType, eventData);
    
    def onHUDInformation(self, HUDEvent):
        pass

Zero.RegisterComponent("HUDDispatcher", HUDDispatcher)