import Zero
import Events
import Property
import VectorMath

import Action
import math #math.radians()


class HoverSprite:
    Sprite = Property.SpriteSource()
    Offset = Property.Vector3(default = VectorMath.Vec3(0,2,0.1))
    Rotate = Property.Vector3()
    Scale =  Property.Vector3(default = VectorMath.Vec3(1,1,1))
    FadeInTime = Property.Float(default = 0.5)
    FadeOutTime = Property.Float(default = 0.5)
    
    EventType = Property.String()
    Duration = Property.Float(default = 1.5)
    SpaceEvent = Property.Bool(default = True)
    OwnerEvent = Property.Bool(default = False)
    
    Delay = Property.Float(default = 0)
    
    def Initialize(self, initializer):
        if not self.EventType == "":
            if self.OwnerEvent:
                Zero.Connect(self.Owner, self.DetectEventType, self.OnActivation)
            elif self.SpaceEvent:
                Zero.Connect(self.Space, self.DetectEventType, self.OnActivation)
        else:
            Zero.Connect(self.Owner, Events.CollisionStarted, self.onCollision)
            Zero.Connect(self.Owner, Events.CollisionEnded, self.onCollisionEnd)
    
    def onCollision(self, cEvent):
        other = cEvent.OtherObject
        
        if other.Player and not self.Sprite.Name == "DefaultSprite":
            self.popUp()
    
    def popUp(self):
        if not self.Sprite.Name == "DefaultSprite":
            self.icon = self.Space.CreateAtPosition("Menu_ControllerPlugin", self.Owner.Transform.Translation + self.Offset)
            self.icon.Sprite.SpriteSource = self.Sprite
            self.icon.Sprite.Visible = False
            
            rotX = math.radians(self.Rotate.x)
            rotY = math.radians(self.Rotate.y)
            rotZ = math.radians(self.Rotate.z)
            self.icon.Transform.RotateAnglesLocal(VectorMath.Vec3(rotX, rotY, rotZ))
            
            self.icon.Transform.Scale = self.Scale
            
            seq = Action.Sequence(self.Owner)
            
            Action.Delay(seq, self.Delay)
            Action.Call(seq, self.icon.Fader.FadeIn, (self.FadeInTime))
        #endif
    #enddef
    
    def popDown(self):
        if self.icon:
            self.icon.Fader.FadeOut(self.FadeOutTime)
            seq = Action.Sequence(self.Owner)
            Action.Delay(seq, self.icon.Fader.FadeOutDuration)
            Action.Call(seq, self.icon.Destroy)
    
    def onCollisionPersist(self, cEvent):
        other = cEvent.OtherObject
    
    def onCollisionEnd(self, cEvent):
        other = cEvent.OtherObject
        
        if other.Player and self.icon:
            self.popDown()
            #self.icon.Fader.FadeOut(self.FadeOutTime)
            #seq = Action.Sequence(self.Owner)
            #Action.Delay(seq, self.icon.Fader.FadeOutDuration)
            #Action.Call(seq, self.icon.Destroy)
    
    def OnActivation(self, aEvent):
        self.popUp()
        
        seq = Action.Sequence(self.Owner)
        
        Action.Delay(seq, self.Duration)
        Action.Call(seq, self.popDown)

Zero.RegisterComponent("HoverSprite", HoverSprite)