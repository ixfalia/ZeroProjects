import Zero
import Events
import Property
import VectorMath

class Key:
    DebugMode = Property.Bool(default = True)
    KeyID = Property.Int(default = 0)
    KeyName = Property.String()
    isMultiuse = Property.Bool(default = False)
    isUsed = Property.Bool(default = False)
    
    BroadCastOnEvent = Property.String()
    SpaceEvent = Property.Bool(default = True)
    OwnerEvent = Property.Bool(default = False)
    BroadcastToHUD = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollisionStarted)
        
        if not self.BroadCastOnEvent == "":
            if self.SpaceEvent:
                Zero.Connect(self.Space, self.BroadCastOnEvent, self.onKeyEvent)
            if self.OwnerEvent:
                Zero.Connect(self.Owner, self.BroadCastOnEvent, self.onKeyEvent)
    
    def onCollisionStarted(self, CollisionEvent):
        if not self.isUsed or self.isMultiuse:
            other = CollisionEvent.OtherObject
            
            if other.Lock:
                if self.DebugMode:
                    print("Key: Lock Collision Detected")
                    
                unlocked = other.Lock.Unlock(self.KeyID)
                
                if unlocked:
                    self.isUsed =  True
        #endif
    #enddef
    
    def onKeyEvent(self, kEvent):
        self.broadCastKey()
    
        #makes and event to dispatch to the space, all listening locks will unlock with it.
    def broadCastKey(self):
        if not self.isUsed or self.isMultiuse:
            KeyEvent = Zero.ScriptEvent()
            
            KeyEvent.KeyID = self.KeyID
            KeyEvent.KeyName = self.KeyName
            #KeyEvent.KeyState = self.KeyState
            
            self.Space.DispatchEvent("KeyEvent", KeyEvent)
            self.Owner.DispatchEvent("KeyEvent", KeyEvent)
            
            if self.Owner.HUDEventDispatcher:
                self.Owner.HUDEventDispatcher.DispatchHUDEvent("KeyEvent", KeyEvent)
                
            
            self.isUsed =  True
            
            if self.DebugMode:
                print("KeyID:", self.KeyID, "is broadcasted")
        #endif

Zero.RegisterComponent("Key", Key)