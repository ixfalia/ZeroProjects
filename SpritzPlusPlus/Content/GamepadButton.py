import Zero
import Events
import Property
import VectorMath

ButtonID = 0

class GamepadButton:
    DebugMode = Property.Bool(default = True)
    Active = Property.Bool(default = True)
    
    spaceEvents = Property.Bool(default = True)
    ownerEvents = Property.Bool(default = True)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        self.Selected = False
        
        if self.spaceEvents:
            Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
        if self.ownerEvents:
            Zero.Connect(self.Owner, "myGamepadEvent", self.onGamepad)
        
        self.ComponentName = "GamepadButton"
        
        global ButtonID
        self.ID = ButtonID
        ButtonID += 1
        
        if self.Owner.SpriteText:
            self.Owner.SpriteText.Visible = self.DebugMode
            self.Owner.SpriteText.Text = "{0}".format(self.ID)
        
        self.ActivateButtons = [Zero.Buttons.A, Zero.Buttons.Start]
        
        e = Zero.ScriptEvent()
        e.ID = self.ID
        e.Object = self.Owner
        self.Space.DispatchEvent("GamepadButtonInit", e)
    
    def onLevel(self, lEvent):
       global ButtonID
       ButtonID = 0
    
    def onGamepad(self, gEvent):
        if not self.Active:
            #raise
            return
        
        for button in self.ActivateButtons:
            if button == gEvent.Button:
                ButtonActivateEvent = Zero.ScriptEvent()
                
                if self.spaceEvents:
                    self.Space.DispatchEvent("ActivateButton", ButtonActivateEvent)
                
                self.Owner.DispatchEvent("ActivateButton", ButtonActivateEvent)
    
    def ActivateSpaceEvents(self):
        if self.spaceEvents:
            return
        
        self.spaceEvents = True
        Zero.Connect(self.Space, "myGamepadEvent", self.onGamepad)
    
    def ActivateOwnerEvents(self):
        if self.ownerEvents:
            return
        
        self.ownerEvents = True
        Zero.Connect(self.Owner, "myGamepadEvent", self.onGamepad)
    
    def DeactivateSpaceEvents(self):
        if not self.spaceEvents:
            return
        
        self.spaceEvents = False
        Zero.Disconnect(self.Space, "myGamepadEvent", self.onGamepad)
    
    def DeactivateOwnerEvents(self):
        if not self.spaceEvents:
            return
        
        self.ownerEvents = False
        Zero.Disconnect(self.Owner, "myGamepadEvent", self.onGamepad)
    
    def ActivateEvents(self):
        self.ActivateOwnerEvents()
        self.ActivateSpaceEvents()
    
    def DeactivateEvents(self):
        self.DeactivateOwnerEvents()
        self.DeactivateSpaceEvents()
    
#endclass

Zero.RegisterComponent("GamepadButton", GamepadButton)