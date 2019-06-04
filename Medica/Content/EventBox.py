import Zero
import Events
import Property
import VectorMath

class EventBox:
    Archetype = Property.Archetype()
    NameParameter = Property.String()
    TextParameter = Property.TextBlock
    DetectHover = Property.Bool(default = False)
    Offset = Property.Vector3(default = VectorMath.Vec3(0,2,0))
    
    Active = Property.Bool(default = False)
    Used = Property.Bool(default = False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "MouseActivateEvent", self.onActivate)
        Zero.Connect(self.Owner, Events.MouseExit, self.onExit)
        Zero.Connect(self.Owner, "UsedEvent", self.onUsed)
        Zero.Connect(self.Owner, "DeactivateEvent", self.onDeactivate)
        
        self.Created = None
        
        if not self.NameParameter:
            self.NameParameter = "Undefined Name"
        if not self.Archetype:
            self.Archetype = "HoverText"
    
    def onActivate(self, e):
        myTransl = self.Owner.Transform.Translation
        position = VectorMath.Vec3(myTransl.x, myTransl.y, 3)
        
        if self.Archetype:
            if self.Created:
                self.Created.Destroy()
            
            self.Created = self.Space.CreateAtPosition(self.Archetype, position)
    
    def onExit(self, e):
        #if self.Created:
            #self.Created.Destroy()
        pass
    
    def onUsed(self, e):
        pass
    
    def onDeactivate(self, e):
        pass

Zero.RegisterComponent("EventBox", EventBox)