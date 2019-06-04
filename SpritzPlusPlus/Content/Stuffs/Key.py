import Zero
import Events
import Property
import VectorMath

class Key:
    DebugMode = Property.Bool(default = True)
    KeyID = Property.Int(default = 0)
    isMultiuse = Property.Bool(default = False)
    isUsed = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollisionStarted)
    
    def onCollisionStarted(self, CollisionEvent):
        if not self.isUsed or self.isMultiuse:
            other = CollisionEvent.GetOtherObject(self.Owner)
            
            if other.Lock:
                if self.DebugMode:
                    print("Key: Lock Collision Detected")
                    
                other.Lock.Unlock(self.KeyID)
                self.isUsed =  True
        #endif
    #enddef
    
        #makes and event to dispatch to the space, all listening locks will unlock with it.
    def broadCastKey(self):
        if not self.isUsed or self.isMultiuse:
            KeyEvent = Zero.ScriptEvent()
            
            KeyEvent.KeyID = self.KeyID
            
            self.Space.DispatchEvent("KeyEvent", KeyEvent)
            
            self.isUsed =  True
            
            if self.DebugMode:
                print("KeyID:", self.KeyID, "is broadcasted")
        #endif

Zero.RegisterComponent("Key", Key)