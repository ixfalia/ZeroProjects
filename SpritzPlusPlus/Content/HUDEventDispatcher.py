import Zero
import Events
import Property
import VectorMath

class HUDEventDispatcher:
    def Initialize(self, initializer):
        pass
    
    def DispatchHUDEvent(self, EventName, Event):
        HUDSpace = self.GameSession.FindSpaceByName("HUDSpace")
        
        if HUDSpace:
            HUDSpace.DispatchEvent(EventName, Event)
        else:
            print("HUDEventDispatcher.SendtoHUD(): HUD Space not found!")
    
    #Sends an event to the HUD Space
    def SendtoHUD(self, EventName, Event):
        self.DispatchHUDEvent(EventName, Event)

Zero.RegisterComponent("HUDEventDispatcher", HUDEventDispatcher)