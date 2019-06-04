import Zero
import Events
import Property
import VectorMath

class MousePrizeBox:
    def DefineProperties(self):
        #self.Lives = Property.Int(9)
        self.used = Property.Bool(default = False)
        
        self.detectRightClick = Property.Bool(default = True)
        self.PrizeType = Property.Archetype()
        self.Offset = Property.Vector3(default = VectorMath.Vec3())
        
        self.ClicksBeforeUse = Property.Uint(default = 0)
        pass

    def Initialize(self, initializer):
        #Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.self, Events.MouseDown, self.onMouseDown)
        
        self.Clicks = 0
        pass

    def OnLogicUpdate(self, UpdateEvent):
        pass
    
    def onMouseDown(self, mEvent):
        mouse = mEvent.Mouse
        if self.detectRightClick and mouse.IsButtonDown(Zero.MouseButtons.Right):
            self.Clicks += 1
            self.dink()
            
            if self.Clicks >= self.ClicksBeforeUse:
                self.dropPrize()
    
    def dropPrize(self):
        if self.used:
            return
        
        self.Space.CreateAtPosition(self.PrizeType, self.Owner.Transform.Translation + self.Offset)
        self.used = True
    
    def dink(self):
        self.Space.CreateAtPosition("Effect_Search", self.Owner.Transform.Translation)
        self.Owner.SoundEmitter.PlayCue("dink")

Zero.RegisterComponent("MousePrizeBox", MousePrizeBox)