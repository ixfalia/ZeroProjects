import Zero
import Events
import Property
import VectorMath

class HUDFlowerText:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, "FlowerCountEvent", self.onFlowerCreate)
        Zero.Connect(self.Space, "FlowerGet", self.onFlowerGet)
        
        self.TotalFlowers = 0
        self.FlowerCount = 0
        
        self.updateText()
    
    def onFlowerCreate(self, flowerEvent):
        self.TotalFlowers += 1
        
        self.updateText()
    
    def onFlowerGet(self, flowerEvent):
        self.FlowerCount += 1
        
        FlowerEvent = Zero.ScriptEvent()
        
        FlowerEvent.TotalFlowers = self.TotalFlowers
        FlowerEvent.FlowerCount = self.FlowerCount
        
        self.Space.DispatchEvent("FlowerEvent", FlowerEvent)
        
        if self.FlowerCount >= self.TotalFlowers:
            self.Space.DispatchEvent("AllFlowers", FlowerEvent)
        
        self.updateText()
    
    def updateText(self):
        self.Owner.SpriteText.Text = "%d / %d" % (self.FlowerCount, self.TotalFlowers)

Zero.RegisterComponent("HUDFlowerText", HUDFlowerText)