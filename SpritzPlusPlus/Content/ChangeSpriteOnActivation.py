import Zero
import Events
import Property
import VectorMath

class ChangeSpriteOnActivation:
    MainSprite = Property.SpriteSource()
    AnotherSprite = Property.SpriteSource("")
    DetectEventType = Property.String(default = "")
    SpaceEvent = Property.Bool(default = False)
    OwnerEvent = Property.Bool(default = True)
    
    EventFunction = Property.Bool(default = False)
    
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
        #print("ChangeOnActivation.OnActivation()")
        if not self.MainSprite.Name == "DefaultSprite":
            self.Owner.Sprite.SpriteSource = self.MainSprite
        if not self.AnotherSprite.Name == "DefaultSprite":
            self.Owner.PutAnotherSprite.CreateNewSprite(self.AnotherSprite)
        
        if Event.fn:
            Event.fn(self)

Zero.RegisterComponent("ChangeSpriteOnActivation", ChangeSpriteOnActivation)