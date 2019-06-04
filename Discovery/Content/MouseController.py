import Zero
import Events
import Property
import VectorMath


class MouseController:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.Debug = Property.Bool(default = False)
        pass

    def Initialize(self, initializer):
        if not self.Owner.Reactive:
            raise
        
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.MouseEnter, self.onMouseEnter)
        Zero.Connect(self.Owner, Events.MouseUpdate, self.onMouseUpdate)
        Zero.Connect(self.Owner, Events.MouseExit, self.onMouseExit)
        Zero.Connect(self.Owner, Events.RightMouseDown, self.onRightMouseDown)
        Zero.Connect(self.Owner, Events.RightMouseUp, self.onRightMouseUp)
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onMouseEnter(self, mEvent):
        self.isMouseOver = True
        self.printState(mEvent)
        
        self.sendEvent("myMouseEnter", mEvent)
        pass
    
    def onMouseExit(self, mEvent):
        self.isMouseOver = False
        self.printState(mEvent)
        
        self.sendEvent("myMouseExit", mEvent)
        pass
    
    def onMouseUpdate(self, mEvent):
        if not self.isMouseOver:
            return
        
        if mEvent.Mouse.IsButtonDown(Zero.MouseButtons.Right):
            pass
        
        self.sendEvent("myMouseUpdate", mEvent)
        pass
    
    def onRightMouseDown(self, mEvent):
        self.Owner.DispatchEvent("myRightMouseDown", Zero.ScriptEvent())
        self.printState(mEvent)
        
        self.sendEvent("myMouseEnter", mEvent)
        pass
    
    def onRightMouseUp(self, mEvent):
        if not self.isMouseOver:
            return
        
        self.Owner.DispatchEvent("myRightMouseUp", Zero.ScriptEvent())
        self.printState(mEvent)
        
        self.sendEvent("myMouseRightMouseUp", mEvent)
        pass
    
    def onLeftMouseUp(self, mEvent):
        if not self.isMouseOver:
            return
        
        self.Owner.DispatchEvent("myLeftMouseUp", Zero.ScriptEvent())
        self.printState(mEvent)
        
        self.sendEvent("myLeftMouseUp", mEvent)
    
    def onLeftMouseDown(self, mEvent):
        if not self.isMouseOver:
            return
        
        self.Owner.DispatchEvent("myLeftMouseDown", Zero.ScriptEvent())
        self.printState(mEvent)
        
        self.sendEvent("myLeftMouseDown", mEvent)
    
    def printState(self, mEvent):
        if not self.Debug:
            return
        
        #print("{} Mouse Event: {}".format(self.Owner.Name, mEvent.EventId))
    
    def sendEvent(self, eventType, mouseEvent):
        e = Zero.ScriptEvent()
        e.EventID =  eventType
        e.MEvent = mouseEvent
        
        self.Owner.DispatchEvent("myMouseEvent", e)

Zero.RegisterComponent("MouseController", MouseController)