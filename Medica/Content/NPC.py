import Zero
import Events
import Property
import VectorMath

class NPC:
    NPCName = Property.String()
    Quests = Property.String()
    
    ChatterText = Property.String()
    Radius = Property.Float()
    
    def Initialize(self, initializer):
        Zero.Connect(Zero.Game, "RenownEvent", self.onRenown)
        Zero.Connect(Zero.Game, "DataFlagEvent", self.onFlag)
        
        self.FellowshipLevel = 0
        self.Chatter = None
        
        if self.Owner.HoverText:
            self.Owner.HoverText.Text = self.NPCName
        
        if not self.ChatterText == "":
            self.Chatter = self.Space.CreateAtPosition("RadiusTrigger", self.Owner.Transform.Translation)
            self.Chatter.CreateOnCollide.chatText = self.ChatterText
    
    def onRenown(self):
        pass
    
    def onFlag(self, e):
        self.checkRequirements()
    
    def checkRequirements(self):
        pass

Zero.RegisterComponent("NPC", NPC)