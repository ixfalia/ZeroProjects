import Zero
import Events
import Property
import VectorMath

import Action

class PushMessage:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "MouseActivateEvent", self.onActivate)
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.onCollisionPersist)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.onCollisionEnd)
        Zero.Connect(self.Space, "PushDelete", self.onPushDelete)
        #Zero.Connect(self.Space, Events.LogicUpdate, self.onUpdate)
        
        self.Velocity = VectorMath.Vec3(0,6,0)
        
        self.Owner.RigidBody.Velocity = self.Velocity
        
        self.Name = None
        self.Message = None
        self.Icon = None
        self.Color = None
        self.BackColor = None
        self.Sound = None
        self.Amount = None
        self.Item = None
    
    def setData(self, Name, Message, Icon, Color, BackColor = None, sound = None, amount = None):
        if BackColor:
            self.Owner.Sprite.Color = BackColor
        
        text = self.Owner.FindChildByName("entryText")
        icon = self.Owner.FindChildByName("entryIcon")
        
        outputText = ""
        
        if Icon:
            icon.Sprite.SpriteSource = Icon
        if Color:
            icon.Sprite.Color = Color
        if Name:
            outputText += "{}: ".format(Name)
        if Message:
            outputText += Message
        
        self.Name = Name
        self.Message = Message
        self.Icon = Icon
        self.Color = Color
        
        if BackColor:
            self.BackColor= BackColor
        if sound:
            self.Sound = sound
        if amount:
            self.Amount = amount
        
        text.SpriteText.Text = outputText
        
        if not sound:
            self.Owner.SoundEmitter.Play()
        elif not sound == None:
            self.Owner.SoundEmitter.PlayCue(sound)
    
    def onActivate(self, e):
        self.Owner.Fader.FadeDestroy()
        
        Zero.Disconnect(self.Space, "PushDelete", self.onPushDelete)
        
        seq =  Action.Sequence(self.Owner)
        Action.Delay(seq, self.Owner.Fader.FadeOutDuration)
        Action.Call(seq, self.Space.DispatchEvent, ("PushDelete", e))
    
    def onUpdate(self, e):
        self.Owner.RigidBody.Velocity = self.Velocity
    
    def onCollisionPersist(self, e):
        other = e.OtherObject
        
        if not other.BoxCollider:
            return
        
        if other.PushMessage:
            if other.PushMessage.Item == self.Item:
                text = self.Owner.FindChildByName("entryText")
                
                if self.Amount and other.PushMessage.Amount:
                    self.Amount += other.PushMessage.Amount
                
                self.Message = "Obtained {} x{}.".format(self.Item, self.Amount)
                text.SpriteText.Text = "{}: {}".format(self.Name, self.Message)
                
                other.BoxCollider.SendsEvents = False
                other.Destroy()
                self.Owner.RigidBody.Velocity = self.Velocity
                return
        
        if not other.BoxCollider.CollisionGroup.Name == "UIItem":
            return
        
        ray = VectorMath.Ray()
        ray.Start = self.Owner.Transform.Translation
        ray.Direction = VectorMath.Vec3(0,1,0)
        
        object = self.Space.PhysicsSpace.CastRayFirst(ray)
        
        if object:
            if object.BoxCollider.CollisionGroup.Name == "UIItem":
                self.Owner.RigidBody.Velocity = VectorMath.Vec3()
                self.Owner.BoxCollider.CollisionGroup = "UIItem"
    
    def onCollisionEnd(self, e):
        other = e.OtherObject
        self.Owner.RigidBody.Velocity = self.Velocity
    
    def onPushDelete(self, e):
        self.Owner.RigidBody.Velocity = self.Velocity

Zero.RegisterComponent("PushMessage", PushMessage)