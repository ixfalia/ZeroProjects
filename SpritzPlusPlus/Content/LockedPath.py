import Zero
import Events
import Property
import VectorMath

class LockedPath:
    EventListened = Property.String()
    SpaceEvent = Property.Bool(default = True)
    OwnerEvent = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        if not self.EventListened == "":
            if self.SpaceEvent:
                Zero.Connect(self.Space, self.EventListened, self.onKeyEvent)
            if self.OwnerEvent:
                Zero.Connect(self.Owner, self.EventListened, self.onKeyEvent)
            #endif
        #endif
    #end Initialize()
    
    def onKeyEvent(self, kEvent):
        print("LockedPath.onKeyEvent(): Lock Event Received~!")
        self.Owner.PathFollower.Reset()
        self.Owner.PathFollower.Paused = False
    #end onKeyEvent()
#end Class

Zero.RegisterComponent("LockedPath", LockedPath)