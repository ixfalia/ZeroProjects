import Zero
import Events
import Property
import VectorMath

class CheckpointManager:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "CheckpointEvent", self.onCheckpointEvent)
        
        self.CheckpointCount = 0
    
    def onCheckpointEvent(self, cEvent):
        pass

Zero.RegisterComponent("CheckpointManager", CheckpointManager)