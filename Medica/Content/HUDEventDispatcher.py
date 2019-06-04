import Zero
import Events
import Property
import VectorMath

class HUDEventDispatcher:
    Debug = Property.Bool(default=True)
    def Initialize(self, initializer):
        if self.Owner.Space:
            Zero.Connect(self.Space, "HUDEvent", self.onHUDEvent)
    
    def DispatchHUDEvent(self, EventName, Event):
        HUDSpace = Zero.Game.FindSpaceByName("HUDSpace")
        
        if HUDSpace:
            HUDSpace.DispatchEvent(EventName, Event)
        else:
            print("HUDEventDispatcher.SendtoHUD(): HUD Space not found!")
    
    #Sends an event to the HUD Space
    def SendtoHUD(self, EventName, Event):
        self.DispatchHUDEvent(EventName, Event)
    
    def onHUDEvent(self, Event):
        self.DispatchHUDEvent(Event.Name, Event.Event)
        #raise

Zero.RegisterComponent("HUDEventDispatcher", HUDEventDispatcher)