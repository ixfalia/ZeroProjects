import Zero
import Events
import Property
import VectorMath

import TextParser

#String Formats
## Name:State, Name2:OtherState

class ParameterLock:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Active = Property.Bool(default = True)
        self.Debug = Property.Bool(default = False)
        self.ListenFor = Property.String()
        self.LockID = Property.Int()
        #self.isLocked = Property.Bool(default = True)
        self.isListening = Property.Bool(default = True)
        pass

    def Initialize(self, initializer):
        self.ListeningList = {}
        self.ListeningState = {} #For a lock to unlock, all elements in the dictionary should be "True"
        
        #Zero.Connect(self.Owner, "LockEvent", self.onLock)
        #Zero.Connect(self.Owner, "UnLockEvent", self.onUnlock)
        Zero.Connect(self.Space, "KeyEvent", self.onKey)
        Zero.Connect(self.Owner, "KeyEvent", self.onKey)
        
        if not self.ListenFor == "":
            parameters = TextParser.ParseParameterText(self.ListenFor, self.Owner.Name)
            self.ListeningList = parameters
            
            for key in self.ListeningList.keys():
                self.ListeningState[key] = False
            #print(self.Owner.Name, self.ListeningList)
        pass
    
    def onKey(self, kEvent):
        id = kEvent.KeyID
        type = kEvent.KeyName
        isPowered = kEvent.Powered
        
        if type in self.ListeningState.keys():
            self.ListeningState[type] = isPowered == self.ListeningList[type]
            
            if self.Debug:
                print("\tListeningState[{}] set to: {}".format(self.Owner.Name, type, self.ListeningState[type]))
                #raise
        
        self.evaluateLocks()
    
    def onLock(self, lEvent):
        type = lEvent.LockID
        
        if type == self.LockType:
            self.isLocked = True
    
    def onUnlock(self, lEvent):
        type = lEvent.LockID
        
        if type == self.LockType:
            self.isLocked = False
    
    def evaluateLocks(self):
        #print(self.ListeningState)
        lockEvent = Zero.ScriptEvent()
        lockEvent.LockID = self.LockID
        lockEvent.LockName = self.Owner.Name
        
        if self.Owner.Name == "Projector":
            #print(self.ListeningState)
            #raise
            pass
        if not (False in self.ListeningState.values()): #when all states are true, this lock is open
            self.isLocked = False
            self.isOpen = True
            #raise
        else:
            self.isLocked = True
            self.isOpen = False
        
        lockEvent.isLocked = self.isLocked
        lockEvent.isOpen = self.isOpen
        
        if self.Debug:
            #print("{} (ParameterLock): isLocked: {}".format(self.Owner.Name, self.isLocked))
            pass
        
        self.Owner.DispatchEvent("LockEvent", lockEvent)

Zero.RegisterComponent("ParameterLock", ParameterLock)