import Zero
import Events
import Property
import VectorMath

class NPC_Mayor:
    def Initialize(self, initializer):
        Zero.Connect(Zero.Game, "DataFlagEvent", self.onFlag)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        
    
    def onLevel(self, e):
        #Zero.Game.Journal.setFlagState("Help The Town", True)
        pass
    def onFlag(self, e):
        #raise
        pass

Zero.RegisterComponent("NPC_Mayor", NPC_Mayor)