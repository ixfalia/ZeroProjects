import Zero
import Events
import Property
import VectorMath

class ChangeOnActivation:
    MainSprite = Property.String(default = "")
    AnotherSprite = Property.String(default = "")
    DetectEventType = Property.String(default = "")
    SpaceEvent = Property.Bool(default = False)
    OwnerEvent = Property.Bool(default = True)
    
    def Initialize(self, initializer):
        #print("ChangeOnActivation.Init()")
        if not self.DetectEventType == "":
            #print(self.DetectEventType, "Event connected to this component.")
            if self.OwnerEvent:
                Zero.Connect(self.Owner, self.DetectEventType, self.OnActivation)
            elif self.SpaceEvent:
                Zero.Connect(self.Space, self.DetectEventType, self.OnActivation)
        else:
            Zero.Connect(self.Owner, "FlowerGet", self.OnActivation)
    
    def OnActivation(self, Event):
        print("ChangeOnActivation.OnActivation()")
        if not self.MainSprite == "":
            self.Owner.Sprite.SpriteSource = self.MainSprite
            pass
        if not self.AnotherSprite == "":
            self.Owner.PutAnotherSprite.CreateNewSprite(self.AnotherSprite)

Zero.RegisterComponent("ChangeOnActivation", ChangeOnActivation)