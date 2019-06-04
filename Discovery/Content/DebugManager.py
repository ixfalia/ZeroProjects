import Zero
import Events
import Property
import VectorMath

class DebugManager:
    def DefineProperties(self):
        self.DebugMode = Property.Bool(default = False)
        self.DebugExtreme = Property.Bool(default = False)
        pass

    def Initialize(self, initializer):
        Zero.Connect(self.GameSession, "DebugToggle", self.onDebugToggle)
        Zero.Connect(self.GameSession, "DebugExtremeToggle", self.onDebugExtremeToggle)
        
        pass

    def onDebugToggle(self, DebugEvent):
        self.DebugMode = not self.DebugMode
        
        print(":|[Game]|:\n ------------------ \n\t DebugMode: set to {}".format(self.DebugMode))
        
        self.debugUpdate()
    
    def onDebugExtremeToggle(self, DebugEvent):
        self.DebugExtreme = not self.DebugExtreme
        
        print(":|[Game]|:\n ------------------ \n\t DebugExtreme: set to {}".format(self.DebugExtreme))
        
        self.debugUpdate()
    
    def debugUpdate(self):
        
        DebugEvent = Zero.ScriptEvent()
        
        DebugEvent.DebugMode = self.DebugMode
        DebugEvent.DebugExtreme = self.DebugExtreme
        
        self.Owner.DispatchEvent("DebugUpdate", DebugEvent)

Zero.RegisterComponent("DebugManager", DebugManager)