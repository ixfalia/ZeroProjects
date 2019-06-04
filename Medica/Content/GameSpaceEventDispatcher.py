import Zero
import Events
import Property
import VectorMath

class GameSpaceEventDispatcher:
    def Initialize(self, initializer):
        if self.Owner.Space:
            Zero.Connect(self.Space, "HUDMakerEvent", self.onHUDEvent)
            Zero.Connect(self.Space, "GameSpaceEvent", self.onGameSpaceEvent)
        else:
            Zero.Connect(self.Owner, "HUDMakerEvent", self.onHUDEvent)
            Zero.Connect(self.Owner, "GameSpaceEvent", self.onGameSpaceEvent)
        
        self.gameSpace = None
    
    def DispatchGameSpaceEvent(self, EventName, Event):
        gSpace = Zero.Game.FindSpaceByName("GameSpace")
        
        if not gSpace:
            if self.gameSpace:
                gSpace = self.gameSpace
            else:
                #raise
                return
        
        gSpace.DispatchEvent(EventName, Event)
    
    def onHUDEvent(self, e):
        print("GameEventDispatcher: HUDMaker Event Recieved. gameSpace set.")
        self.gameSpace = e.Space
    
    def onGameSpaceEvent(self, e):
        self.DispatchGameSpaceEvent(e.Name, e.Event)
    
    def blah(self, e):
        raise

Zero.RegisterComponent("GameSpaceEventDispatcher", GameSpaceEventDispatcher)