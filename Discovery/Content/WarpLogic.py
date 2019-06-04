import Zero
import Events
import Property
import VectorMath

class WarpLogic:
    def DefineProperties(self):
        self.Active = Property.Bool(default = False)
        #self.ListeningFor = Property.String()
        self.WarpTo = Property.Cog()
        pass

    def Initialize(self, initializer):
        Listeners = {}
        
        Zero.Connect(self.Owner, "LockEvent", self.onLock)
        
        self.updateChildStatus()
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onActivate(self, aEvent):
        if not aEvent.ID == self.ListeningFor:
            return
        
        self.Active = True
        self.updateChildStatus()
    
    def onDeactivate(self, aEvent):
        if not aEvent.ID == self.ListeningFor:
            return
        
        self.Active = False
        
        self.updateChildStatus()
    
    def updateChildStatus(self):
        self.Owner.SphericalParticleEmitter.Active = self.Active
        self.Owner.Light.Visible = self.Active
        
        for child in self.Owner.Hierarchy.Children:
            if child.Rotator:
                child.Rotator.Active = self.Active
            
            if self.Active:
                child.DispatchEvent("ActivateEvent", Zero.ScriptEvent())
            else:
                child.DispatchEvent("DeactivateEvent", Zero.ScriptEvent())
    
    def onLock(self, lEvent):
        isLocked = lEvent.isLocked
        
        if not isLocked:
            self.activate()
        else:
            self.deactivate()
    
    def activate(self):
        self.Active = True
        
        self.updateChildStatus()
    
    def deactivate(self):
        self.Active = False
        
        self.updateChildStatus()

Zero.RegisterComponent("WarpLogic", WarpLogic)