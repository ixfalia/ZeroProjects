import Zero
import Events
import Property
import VectorMath

class BroadcastButton:
    EventName = Property.String()
    
    spaceEvent = Property.Bool(default = True)
    ownerEvent = Property.Bool(default = False)
    hudEvent = Property.Bool(default = False)
    gameEvent = Property.Bool(default = False)
    parentEvent = Property.Bool(default = False)
    allParentsEvent = Property.Bool(default = False)
    childrenEvent = Property.Bool(default = False)
    allChildrenEvent = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "MouseActivateEvent", self.onActivate)
        
        lsettings = self.Space.FindObjectByName("LevelSettings")
        self.HUDDispatcher = lsettings.HUDEventDispatcher
    
    def onActivate(self, e):
        self.BroadcastEvent()
    
    def BroadcastEvent(self):
        e = Zero.ScriptEvent()
        
        print("\t[[{0}|BroadcastButton]]:".format(self.Owner.Name), self.EventName, "Event dispatched")
        
        if self.spaceEvent:
            self.Space.DispatchEvent(self.EventName, e)
        if self.ownerEvent:
            self.Owner.DispatchEvent(self.EventName, e)
        if self.hudEvent:
            self.HUDDispatcher.DispatchEvent(self.EventName, e)
        if self.gameEvent:
            Zero.Game.DispatchEvent(self.EventName, e)
        if self.parentEvent:
            self.Owner.Parent.DispatchEvent(self.EventName, e)
        if self.allParentsEvent:
            self.Owner.Parent.DispatchUp(self.EventName, e)
        if self.childrenEvent:
            for child in self.Owner.Children:
                child.DispatchEvent(self.EventName, e)
        if self.allChildrenEvent:
            self.Owner.DispatchDown(self.EventName, e)

Zero.RegisterComponent("BroadcastButton", BroadcastButton)