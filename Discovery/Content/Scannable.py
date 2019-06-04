import Zero
import Events
import Property
import VectorMath

import Action
import Color

class ScanObject:
    def DefineProperties(self):
        self.Resources = Property.ResourceTable(default = "Material")
        self.MarvelName = Property.String(default = "")
        self.TextBody = Property.TextBlock()
        pass

    def Initialize(self, initializer):
        if not self.Owner.Reactive:
            raise
        
        self.isMouseOver = False
        self.chargeTimer = 0.0
        self.lastDT = 0.0
        self.ChargeTime = 1.5
        self.isCharging = False
        
        self.reticle = None
        self.isReady = False
        self.gotMe = False
        
        #Mouse Handlers
        #Zero.Connect(self.Owner, "myMouseEnter", self.onMouseEnter)
        #Zero.Connect(self.Owner, "myMouseExit", self.onMouseExit)
        #Zero.Connect(self.Owner, "myRightMouseDown", self.onRightMouseDown)
        #Zero.Connect(self.Owner, "myRightMouseDown", self.onRightMouseUp)
        #Zero.Connect(self.Owner, "myMouseEvent", self.onMyMouse)
        
        Zero.Connect(self.Owner, Events.RightMouseDown, self.onRightMouseDown)
        Zero.Connect(self.Owner, Events.RightMouseUp, self.onRightMouseUp)
        Zero.Connect(self.Owner, Events.MouseEnter, self.onMouseEnter)
        Zero.Connect(self.Owner, Events.MouseExit, self.onMouseExit)
        Zero.Connect(self.Owner, Events.MouseUpdate, self.onMouseUpdate)
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        Zero.Connect(self.Space, Events.LevelStarted, self.onLevel)
        pass
    
    def onUpdate(self, uEvent):
        self.lastDT = uEvent.Dt
    
    def onLevel(self, lEvent):
        mEvent = Zero.ScriptEvent()
        mEvent.Name = self.MarvelName
        mEvent.Text = self.TextBody
        mEvent.Object = self.Owner
        self.GameSession.DispatchEvent("MarvelEvent", mEvent)
    
    def onMyMouse(self, mEvent):
        type = mEvent.EventID
        mouseEvent = mEvent.MEvent
        
        if type == "MouseEnter":
            self.onMouseEnter(mouseEvent)
        elif type == "MouseExit":
            self.onMouseExit(mouseEvent)
        elif type == "RightMouseDown":
            self.onRightMouseDown(mouseEvent)
        elif type == "RightMouseUp":
            self.onRightMouseUp(mouseEvent)
    
    def onMouseEnter(self, mEvent):
        if self.Owner.Children:
            self.dispatchEventToChildren("myMouseEnter", mEvent)
        pass
    
    def onMouseExit(self, mEvent):
        if self.Owner.Children:
            self.dispatchEventToChildren("myMouseExit", mEvent)
    
    def onRightMouseDown(self, mEvent):
        if self.gotMe:
            view = self.Space.FindObjectByName("LevelSettings").CameraViewport
            pos = view.ScreenToWorldZPlane(Zero.Mouse.ScreenPosition, 2)
            
            thing = self.Space.CreateAtPosition("AlreadyScanned", pos)
            thing.Celebration.celebrate()
            return
        
        if self.Owner.Children:
            e = Zero.ScriptEvent()
            e.Type = "Light"
            e.Intensity = 1.75
            e.Locked = True
            self.dispatchEventToChildren("ChangeEvent", e)
            
        self.chargeTimer += self.ChargeTime
        self.isCharging = True
        
        #ret = self.Space.FindObjectByName("MouseReticle")
        self.createReticle()
        self.chargeTimer = 0.0
        
        seq = Action.Sequence(self.reticle)
        size = VectorMath.Vec3(0.75,0.75)
        Action.Property(seq, self.reticle.Transform, "Scale", size, self.ChargeTime)
        pass
    
    def onRightMouseUp(self, mEvent):
        if self.gotMe:
            return
        
        if self.chargeTimer >= self.ChargeTime:
            scanEvent = Zero.ScriptEvent()
            
            scanEvent.isMarvel = True
            scanEvent.Name = self.MarvelName
            scanEvent.Discovered = True
            
            self.Space.DispatchEvent("MarvelScanned", scanEvent)
            self.GameSession.DispatchEvent("MarvelEvent", scanEvent)
            self.gotMe = True
            print("Scannable: ping")
        
        self.isCharging = False
        self.chargeTimer = 0.0
        print(self.chargeTimer)
        size = VectorMath.Vec3(1.5,1.5)
        seq = Action.Sequence(self.reticle)
        
        Action.Property(seq, self.reticle.Transform, "Scale", size, self.ChargeTime)
        self.reticle.DestructionTimer.activate()
        pass
    
    def onMouseUpdate(self, mEvent):
        if mEvent.Mouse.IsButtonDown(Zero.MouseButtons.Right):
            self.chargeTimer += self.lastDT
            
            if self.chargeTimer > self.ChargeTime:
                #print("brrbrr")
                #ret = self.Space.FindObjectByName("MouseReticle")
                self.scanReady()
            else:
                #print("whrrrrr")
                pass
    
    def scanReady(self):
        if self.isReady:
            return
        
        center = self.reticle.Children
        blue = Color.Cornflower
        blue = VectorMath.Vec4(blue.r, blue.g, blue.b, 0.75)
        
        for obj in center:
            if obj.Name == "centersquare":
                obj.Sprite.Color = Color.Cornflower.lerp(Color.White, 0.5)
                continue
            
            obj.Sprite.Color = blue
        
        e = Zero.ScriptEvent()
        
        e.Cue = "ScanReady"
        self.Space.DispatchEvent("SoundEvent", e)
        self.isReady = True
    
    def dispatchEventToChildren(self, type, sentEvent):
        for child in self.Owner.Children:
            child.DispatchEvent(type, sentEvent)
    
    def createReticle(self):
        if self.reticle:
            self.reticle.DestructionTimer.activate()
        
        view = self.Space.FindObjectByName("LevelSettings").CameraViewport
        pos = view.ScreenToWorldZPlane(Zero.Mouse.ScreenPosition, 5)
        self.reticle = self.Space.CreateAtPosition("Scanner", pos)

Zero.RegisterComponent("ScanObject", ScanObject)