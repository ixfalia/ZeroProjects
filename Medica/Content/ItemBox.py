import Zero
import Events
import Property
import VectorMath

import Color
import Action

class ItemBox:
    Debug = Property.Bool(default = True)
        #use enum later
    ItemName = Property.String(default = "Undefined Item")
    isUsed = Property.Bool(default = False)
    AmountGiven = Property.Uint(default = 1)
    Limit = Property.Int(default = -1)
    Color = Property.Color()
    FadeOut = Property.Bool(default = True)
    RespawnDuration = Property.Float(default = 65)
    RespawnVariance = Property.Float(default = 10)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "MouseActivateEvent", self.onActivate)
        Zero.Connect(self.Owner, "InactiveEvent", self.onInactive)
        Zero.Connect(self.Owner, "ReactivateEvent", self.onReactivate)
        
        #Zero.Connect(self.Space, "FreezeEvent", self.onFreeze)
        
        Zero.Connect(self.Owner, Events.MouseEnter, self.onMouseEnter)
        Zero.Connect(self.Owner, Events.MouseExit, self.onMouseExit)
        
        self.hoverObject = None
        self.StartingLimit = self.Limit
        
        if not self.ItemName:
            self.ItemName = "Undefined Item"
    
    def onActivate(self, e):
        if self.Limit == -1:
            self.sendItemEvent()
        elif self.Limit - self.AmountGiven >= 0:
            self.Limit -= self.AmountGiven
            self.sendItemEvent()
            
            if self.Limit <= 0:
                self.sendInactiveEvent()
        else:
            self.sendInactiveEvent()
            
    
    def onInactive(self, e):
        #self.Owner.Sprite.Color = Color.OliveDrab
        if self.Owner.Fader:
            self.Owner.Fader.FadeOut()
        self.Owner.Reactive.Active = False
        
        if self.Owner.Collider:
            self.Owner.Collider.Ghost = True
        
        seq = Action.Sequence(self.Owner)
        Action.Delay(seq, self.RespawnDuration)
        Action.Call(seq, self.sendReactivateEvent)
    
    def onReactivate(self, e):
        if self.FadeOut:
            self.Owner.Fader.FadeIn()
        self.Owner.Reactive.Active = True
        
        if self.Owner.Collider:
            self.Owner.Collider.Ghost = False
        
        self.Limit = self.StartingLimit
    
    def sendItemEvent(self):
        e = Zero.ScriptEvent()
        
        e.Name = self.ItemName
        e.Amount = self.AmountGiven
        
        if self.Debug:
            print("\t[[{0}|ItemBox]]:".format(self.Owner.Name), self.AmountGiven, "of", self.ItemName, "was sent out.")
        
        self.Space.DispatchEvent("ItemGetEvent", e)
        Zero.Game.DispatchEvent("ItemGetEvent", e)
    
    def sendInactiveEvent(self):
        e = Zero.ScriptEvent()
        
        self.Owner.DispatchEvent("InactiveEvent", e)
    
    def sendReactivateEvent(self):
        e = Zero.ScriptEvent()
        
        self.Owner.DispatchEvent("ReactivateEvent", e)
    
    def onMouseEnter(self, e):
        self.createHover(e)
    
    def onMouseExit(self, e):
        self.hoverText.Fader.FadeDestroy()
    
    def createHover(self, e = None):
        offset = VectorMath.Vec3(0, 2, 2)
        myPos = self.Owner.Transform.Translation
        
        if self.Owner.MeshCollider:
            lSettings = self.Space.FindObjectByName("LevelSettings")
            pos = lSettings.CameraViewport.ScreenToWorldZPlane(e.Position, 0)
            pos = pos + offset - VectorMath.Vec3(0,1,0)
            self.hoverText = self.Space.CreateAtPosition("HoverText", pos + offset)
            #print(self.Created.Transform.Translation)
            #raise
        else:
            self.hoverText = self.Space.CreateAtPosition("HoverText", myPos + offset)
        
        self.hoverText.SpriteText.Text = self.ItemName

Zero.RegisterComponent("ItemBox", ItemBox)