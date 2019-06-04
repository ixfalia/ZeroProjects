import Zero
import Events
import Property
import VectorMath

class Lock:
    DebugMode = Property.Bool(default= True)
    LockID = Property.Int(default = 0)
    LookingFor = Property.Int(default = -1)
    isLocked = Property.Bool(default = True)
    
    isListening = Property.Bool(default = False) #Determines whether or not this object listens for ranged keys.
    
    def Initialize(self, initializer):
        if self.isListening:
            if self.DebugMode:
                print(self.Owner.Name, "is a listening Lock.")
            Zero.Connect(self.Space, "KeyEvent", self.onKeyEvent)
        
    def onKeyEvent(self, Event):
        self.Unlock(Event.KeyID)
    
    def Unlock(self, KeyID):
        if self.DebugMode:
            #print("Lock.Unlock(): self.isLocked:", self.isLocked)
            print("Lock: Key received is:", KeyID)
        
        if self.isLocked ==  True:
                #if the key is right or the lock or key are wildcards we will unlock the prize
            if(KeyID == self.LookingFor or KeyID == -1 or self.LookingFor == -1):
                if self.DebugMode:
                    print("Lock:", self.LockID, " was unlocked by Key:", KeyID)
                
                isLocked = False
                LockEvent = Zero.ScriptEvent()
                
                LockEvent.LockID = self.LockID
                LockEvent.KeyID = KeyID
                LockEvent.LookingFor = self.LookingFor
                LockEvent.Name = self.Owner.Name
                
                self.Owner.DispatchEvent("LockUnlocked", LockEvent)
                return True
            #endif
        #endif
        
        return False
    #end unlock()
    
    def UnlockAnyways(self):
        if self.DebugMode:
            print("UnloackAnyways(): Yay!")
        
        if self.isLocked == True:
            isLocked = False
            LockEvent = Zero.ScriptEvent()
            
            LockEvent.LockID = self.LockID
            LockEvent.KeyID = -1
            LockEvent.LookingFor = self.LookingFor
            LockEvent.Name = self.Owner.Name
            
            self.Owner.DispatchEvent("LockUnlocked", LockEvent)
        #endif

Zero.RegisterComponent("Lock", Lock)