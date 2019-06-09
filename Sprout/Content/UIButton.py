import Zero
import Events
import Property
import VectorMath

import Action

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class UIButton:
    Active = Property.Bool(default = True)
    Debug = Property.Bool(default = False)
    
    enterState = Property.String(default = Events.MouseEnter)
    
    defaultEvent = Property.String(default = "UIState_Default")
    hoverEvent = Property.String(default = "UIState_Hover")
    activateEvent = Property.String(default = "UIState_Activate")
    rightClickEvent = Property.String(default = "UIState_RClick")
    middleClickEvent = Property.String(default = "UIState_MClick")
    
    State = Property.Enum()
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.MouseEnter, self.onEnter)
        Zero.Connect(self.Owner, Events.MouseExit, self.onExit)
        Zero.Connect(self.Owner, Events.RightMouseUp, self.onRightMouseUp)
        Zero.Connect(self.Owner, Events.RightMouseDown, self.onRightMouseDown)
        Zero.Connect(self.Owner, Events.MouseDown, self.onClick)
        Zero.Connect(self.Owner, Events.MouseUp, self.onClickUp)
        
        self.StartingPosition = self.Owner.Transform.Translation
        self.StartingScale = self.Owner.Transform.Scale
        self.isRightMouseDown = False
    #end init()
    
    def onEnter(self, mEvent):
        self.hoverState()
        
        self.debugPrint("- UIButton.onEnter()");
    
    def onExit(self, mEvent):
        self.defaultState()
        
        self.debugPrint("- UIButton.onExit()");
        pass
    
    def onClick(self, mEvent):
        aEvent = Zero.ScriptEvent()
        aEvent.Mouse =  mEvent.Mouse
        aEvent.MouseState = mEvent
        self.Owner.DispatchEvent(self.activateEvent, aEvent)
        
        self.debugPrint("- UIButton.onClick()");
        pass
    
    def onClickUp(self, mEvent):
        aEvent = Zero.ScriptEvent()
        aEvent.Mouse =  mEvent.Mouse
        aEvent.MouseState = mEvent
        self.Owner.DispatchEvent(self.hoverEvent, aEvent)
        
        self.debugPrint("- UIButton.onClickUp()");
    
    def onRightMouseUp(self, mEvent):
        self.isRightMouseDown = False
        self.hoverState()
        self.debugPrint("- UIButton.onRightMouseUp()");
    
    def onRightMouseDown(self, mEvent):
        self.isRightMouseDown = True
        self.downState()
        self.debugPrint("- UIButton.onRightMouseDown()");
    #end onDOwn
    
    ####################
    ## States
    
    def defaultState(self):
        if not self.Active:
            return
        
        ActivateEvent = Zero.ScriptEvent()
        self.Owner.DispatchEvent(self.defaultEvent, ActivateEvent)
        
        #self.TranslationAction(self.StartingPosition)
    #end DefaultState()
    
    def hoverState(self):
        if not self.Active:
            return
        
        #self.TranslationAction(self.StartingPosition+Vec3(0,1,3))
        
        ActivateEvent = Zero.ScriptEvent()
        self.Owner.DispatchEvent(self.hoverEvent, ActivateEvent)
    
    def downState(self):
        if not self.Active:
            return
        
        ActivateEvent = Zero.ScriptEvent()
        self.Owner.DispatchEvent(self.activateEvent, ActivateEvent)
    #end downState()
    
    #####################
    ## Helper Functions
    
    def TranslationAction(self, end, duration = None):
        if not duration:
            duration = 0.15
        
        target = self.Owner.Transform
        
        group = Action.Sequence(self.Owner)
        #end = end + self.Owner.Transform.Translation
        
        Action.Property(group, target, "Translation", end, duration)
        
        #Action.Property(group, target, "Scale", Vec3(scaleVal,scaleVal, 1), duration)
    
    #debug print adds a detailed name to the front of the desired text
    def debugPrint(self, string):
        if(self.Debug):
            print(self.Owner.ArchetypeName, string);

Zero.RegisterComponent("UIButton", UIButton)