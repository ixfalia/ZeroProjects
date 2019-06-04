import Zero
import Events
import Property
import VectorMath

class MouseBox:
    EventName = Property.String(default = "MouseActivateEvent")
    DetectLeftClick = Property.Bool(default = True)
    DetectRightClick = Property.Bool(default = False)
    DetectMiddleClick = Property.Bool(default = False)
    
    sendReactiveEvent = Property.Bool(default = True)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.MouseDown, self.onMouse)
        Zero.Connect(self.Owner, Events.MiddleMouseDown, self.onMiddleMouse)
        Zero.Connect(self.Owner, Events.RightMouseDown, self.onRightMouse)
        
        Zero.Connect(self.Owner, Events.MouseUp, self.onMouseUp)
        Zero.Connect(self.Owner, Events.MiddleMouseUp, self.onMouseUp)
        Zero.Connect(self.Owner, Events.RightMouseUp, self.onMouseUp)
        
        Zero.Connect(self.Owner, Events.MouseEnter, self.onMouseEnter)
        Zero.Connect(self.Owner, Events.MouseExit, self.onMouseExit)
        
        Zero.Connect(self.Space, "FreezeEvent", self.onFreeze)
        Zero.Connect(self.Space, "UnfreezeEvent", self.onUnfreeze)
        
        self.Paused = False
        
        if not self.EventName:
            self.EventName = "MouseActivateEvent"
    
    def onMouse(self, e):
        if self.DetectLeftClick:
            self.sendActivation()
    
    def onMiddleMouse(self, e):
        if self.DetectMiddleClick:
            self.sendActivation()
    
    def onRightMouse(self, e):
        if self.DetectRightClick:
            self.sendActivation()
    
    def onMouseEnter(self, e):
        if not self.sendReactiveEvent:
            return
        e = Zero.ScriptEvent()
        self.Space.DispatchEvent("ReactiveEnter", e)
    
    def onMouseExit(self, e):
        if not self.sendReactiveEvent:
            return
        e = Zero.ScriptEvent()
        self.Space.DispatchEvent("ReactiveExit", e)
    
    def sendActivation(self):
        if self.Paused:
            return
        
        e = Zero.ScriptEvent()
        
        e.Source = "MouseBox"
        e.Target = "EventBox"
        
        self.Owner.DispatchEvent(self.EventName, e)
    
    def onMouseUp(self, e):
        e = Zero.ScriptEvent()
        self.Owner.DispatchEvent("ReactiveUp", e)
    
    def pause(self, e):
        self.Paused = True
    
    def unPause(self, e):
        self.Paused = False
    
    def onFreeze(self, e):
        self.pause(e)
    
    def onUnfreeze(self, e):
        self.unPause(e)

Zero.RegisterComponent("MouseBox", MouseBox)