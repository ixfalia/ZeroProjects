import Zero
import Events
import Property
import VectorMath

class SproutBroadcaster:
    DebugPrint = Property.Bool(False)
    SproutPlacementEvent = Property.String("SproutClickEvent")
    
    def DefineProperties(self):
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.Space, "GameSpaceEvent", self.onSpaceEvent);
        Zero.Connect(Zero.Mouse, Events.MouseDown, self.onMouseDown);
        Zero.Connect(self.Space, Events.MouseDown, self.onMouseDown);
        
        self.GameSpace = None;
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onSpaceEvent(self, spaceEvent):
        if(spaceEvent.Space):
            self.GameSpace = spaceEvent.Space;
            
            if(self.DebugPrint):
                print("SproutBroadcaster.onSpaceEvent(): Game Space ({}) is found and set!".format(self.GameSpace.Name))
            #endif
        else:
            print("{}.onSpaceEvent(): Space not sent with SpaceEvent!".format(self.Owner.Name))
    #endef onSpaceEvent()
    
    def onMouseDown(self, keyEvent):
        if(not self.GameSpace):
            print("SproutBroadcaster.onMouseDown(): Game Space is not defined.");
            return;
        #endif
        
        sproutEvent = Zero.ScriptEvent();
        
        self.GameSpace.DispatchEvent(self.SproutPlacementEvent, sproutEvent);
        
        if(self.DebugPrint):
            print("SproutBroadcaster.onMouseDown(): Click!")
        #endif
    #endef onMouseDown()

Zero.RegisterComponent("SproutBroadcaster", SproutBroadcaster)