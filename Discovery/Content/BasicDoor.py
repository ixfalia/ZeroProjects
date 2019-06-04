import Zero
import Events
import Property
import VectorMath

class BasicDoor:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        #self.ListeningFor = Property.String()
        self.Active = Property.Bool(default = True)
        self.StartsPowered = Property.Bool(default = False)

    def Initialize(self, initializer):
        self.ListeningList = {}
        self.Powered = self.StartsPowered
        
        Zero.Connect(self.Owner, "LockEvent", self.onLock)
    
    def unpower(self):
        self.Powered = True
        
        self.updateStatus()
    
    def power(self):
        self.Powered = False
        
        self.updateStatus()
    
    def updateStatus(self):
        self.Owner.Model.Visible = self.Powered
        self.Owner.Collider.Ghost = not self.Powered
        
        if self.Owner.Light:
            self.Owner.Light.Active = self.Powered
    
    def evaluateState(self):
        if not False in self.ListeningList.values():
            self.Powered = False
    
    def onLock(self, lEvent):
        if lEvent.isLocked:
            self.unpower()
        else:
            self.power()

Zero.RegisterComponent("BasicDoor", BasicDoor)