import Zero
import Events
import Property
import VectorMath

class TownManager:
    TimeRemaining = Property.Uint(default = 10)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "BuildingSiteEvent", self.onSite)
        Zero.Connect(self.Owner, "RenownEvent", self.onRenown)
        
        self.Renown = 0
        self.Repairs = 0
        self.TotalSites = 0
        
        self.Owner.Journal.setFlagState("Renown", self.Renown)
    
    def onSite(self, e):
        self.TotalSites += 1
    
    def onRenown(self, e):
        self.Renown = e.Amount
        
        self.Owner.Journal.setFlagState("Renown", self.Renown)

Zero.RegisterComponent("TownManager", TownManager)