import Zero
import Events
import Property
import VectorMath

class LightActivator:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.ActivateEvent = Property.String(default = "ActivateEvent")
        self.DeactivateEvent = Property.String(default = "DeactivateEvent")
        self.ChangeEvent = Property.String(default = "ChangeEvent")
        self.LockEvent = Property.Bool(default = True)
        pass
    
    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, self.ActivateEvent, self.onActivate)
        Zero.Connect(self.Owner, self.DeactivateEvent, self.onDeactivate)
        Zero.Connect(self.Owner, self.ChangeEvent, self.onChange)
        
        if self.LockEvent:
            Zero.Connect(self.Owner, "LockEvent", self.onLock)
        
        self.StartingValue = self.Owner.Light.Intensity
        self.Locked = False
    
    def onActivate(self, aEvent):
        if self.Locked:
            return
        
        self.Owner.Light.Visible = True
    
    def onDeactivate(self, aEvent):
        if self.Locked:
            return
        
        self.Owner.Light.Visible = False
    
    def onChange(self, aEvent):
        if aEvent.Intensity:
            self.Owner.Light.Intensity = aEvent.Intensity
        if aEvent.Color:
            self.Owner.Light.Color = aEvent.Color
        if aEvent.Size:
            self.Owner.Light.Size = aEvent.Size
        if aEvent.Range:
            self.Owner.Light.Range = aEvent.Range
        if aEvent.MinRange:
            self.Owner.Light.MinRange = aEvent.MinRange
        if aEvent.Type == "Light" and aEvent.Locked:
            self.Locked = aEvent.Locked
    
    def onLock(self, lEvent):
        isOpen = lEvent.isOpen
        print("LightActivator is Powered:", isOpen)
        
        if isOpen:
            self.onActivate(lEvent)
        else:
            self.onDeactivate(lEvent)

Zero.RegisterComponent("LightActivator", LightActivator)